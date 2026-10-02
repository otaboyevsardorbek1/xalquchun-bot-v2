# bot/services/analytics.py
"""
Analytics va statistika xizmati
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Statistika va analytics xizmati"""
    
    def __init__(self, session):
        self.session = session
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Admin dashboard uchun umumiy statistika
        
        Returns:
            {
                "users": {...},
                "orders": {...},
                "revenue": {...},
                "products": {...}
            }
        """
        from sqlalchemy import select, func
        from bot.db.models import User, Order, Product, OrderItem
        
        stats = {}
        
        # Foydalanuvchilar statistikasi
        users_total = await self.session.scalar(select(func.count(User.id)))
        users_today = await self.session.scalar(
            select(func.count(User.id)).where(
                User.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
            )
        )
        users_this_week = await self.session.scalar(
            select(func.count(User.id)).where(
                User.created_at >= datetime.now() - timedelta(days=7)
            )
        )
        users_blocked = await self.session.scalar(
            select(func.count(User.id)).where(User.blocked == True)
        )
        
        stats["users"] = {
            "total": users_total or 0,
            "today": users_today or 0,
            "this_week": users_this_week or 0,
            "blocked": users_blocked or 0,
            "active": (users_total or 0) - (users_blocked or 0)
        }
        
        # Buyurtmalar statistikasi
        orders_total = await self.session.scalar(select(func.count(Order.id)))
        orders_today = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
            )
        )
        orders_pending = await self.session.scalar(
            select(func.count(Order.id)).where(Order.status == "new")
        )
        orders_completed = await self.session.scalar(
            select(func.count(Order.id)).where(Order.status == "delivered")
        )
        orders_cancelled = await self.session.scalar(
            select(func.count(Order.id)).where(Order.status == "cancelled")
        )
        
        stats["orders"] = {
            "total": orders_total or 0,
            "today": orders_today or 0,
            "pending": orders_pending or 0,
            "completed": orders_completed or 0,
            "cancelled": orders_cancelled or 0
        }
        
        # Daromad statistikasi
        revenue_total = await self.session.scalar(
            select(func.sum(Order.total_amount)).where(
                Order.status.in_(["delivered", "ready"])
            )
        ) or 0
        
        revenue_today = await self.session.scalar(
            select(func.sum(Order.total_amount)).where(
                Order.status.in_(["delivered", "ready"]),
                Order.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
            )
        ) or 0
        
        revenue_this_month = await self.session.scalar(
            select(func.sum(Order.total_amount)).where(
                Order.status.in_(["delivered", "ready"]),
                Order.created_at >= datetime.now().replace(day=1, hour=0, minute=0, second=0)
            )
        ) or 0
        
        stats["revenue"] = {
            "total": float(revenue_total),
            "today": float(revenue_today),
            "this_month": float(revenue_this_month)
        }
        
        # Mahsulotlar statistikasi
        products_total = await self.session.scalar(select(func.count(Product.id)))
        products_available = await self.session.scalar(
            select(func.count(Product.id)).where(Product.is_available == True)
        )
        
        stats["products"] = {
            "total": products_total or 0,
            "available": products_available or 0,
            "unavailable": (products_total or 0) - (products_available or 0)
        }
        
        logger.info("Dashboard statistika olindi")
        return stats
    
    async def get_user_growth(self, days: int = 30) -> List[Dict]:
        """
        Foydalanuvchilar o'sishi (kunlik)
        
        Args:
            days: Necha kunlik ma'lumot
        
        Returns:
            [{"date": "2026-04-01", "count": 5}, ...]
        """
        from sqlalchemy import select, func
        from bot.db.models import User
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Kunlik group by
        result = await self.session.execute(
            select(
                func.date(User.created_at).label("date"),
                func.count(User.id).label("count")
            ).where(
                User.created_at >= start_date
            ).group_by(
                func.date(User.created_at)
            ).order_by(
                func.date(User.created_at)
            )
        )
        
        data = []
        for row in result:
            data.append({
                "date": row.date.strftime("%Y-%m-%d"),
                "count": row.count
            })
        
        logger.info(f"User growth: {len(data)} kunlik ma'lumot")
        return data
    
    async def get_revenue_chart(self, days: int = 30) -> List[Dict]:
        """
        Daromad grafigi (kunlik)
        
        Args:
            days: Necha kunlik ma'lumot
        
        Returns:
            [{"date": "2026-04-01", "amount": 1500000}, ...]
        """
        from sqlalchemy import select, func
        from bot.db.models import Order
        
        start_date = datetime.now() - timedelta(days=days)
        
        result = await self.session.execute(
            select(
                func.date(Order.created_at).label("date"),
                func.sum(Order.total_amount).label("amount")
            ).where(
                Order.created_at >= start_date,
                Order.status.in_(["delivered", "ready"])
            ).group_by(
                func.date(Order.created_at)
            ).order_by(
                func.date(Order.created_at)
            )
        )
        
        data = []
        for row in result:
            data.append({
                "date": row.date.strftime("%Y-%m-%d"),
                "amount": float(row.amount or 0)
            })
        
        logger.info(f"Revenue chart: {len(data)} kunlik ma'lumot")
        return data
    
    async def get_top_products(self, limit: int = 10) -> List[Dict]:
        """
        Eng ko'p sotiladigan mahsulotlar
        
        Args:
            limit: Nechta mahsulot
        
        Returns:
            [{"name": "Mahsulot", "count": 50, "revenue": 1000000}, ...]
        """
        from sqlalchemy import select, func
        from bot.db.models import OrderItem, Product
        
        result = await self.session.execute(
            select(
                Product.name,
                func.sum(OrderItem.quantity).label("count"),
                func.sum(OrderItem.quantity * OrderItem.price).label("revenue")
            ).join(
                Product, OrderItem.product_id == Product.id
            ).group_by(
                Product.name
            ).order_by(
                func.sum(OrderItem.quantity).desc()
            ).limit(limit)
        )
        
        data = []
        for row in result:
            data.append({
                "name": row.name,
                "count": float(row.count or 0),
                "revenue": float(row.revenue or 0)
            })
        
        logger.info(f"Top products: {len(data)} ta mahsulot")
        return data
    
    async def get_orders_by_status(self) -> Dict[str, int]:
        """
        Buyurtmalar holati bo'yicha
        
        Returns:
            {"new": 5, "processing": 3, ...}
        """
        from sqlalchemy import select, func
        from bot.db.models import Order
        
        result = await self.session.execute(
            select(
                Order.status,
                func.count(Order.id).label("count")
            ).group_by(Order.status)
        )
        
        data = {}
        for row in result:
            data[row.status] = row.count
        
        logger.info(f"Orders by status: {data}")
        return data
    
    async def get_user_activity(self, days: int = 7) -> Dict[str, Any]:
        """
        Foydalanuvchilar faolligi
        
        Args:
            days: Necha kunlik ma'lumot
        
        Returns:
            {
                "active_users": 100,
                "orders_per_user": 2.5,
                "avg_order_value": 150000
            }
        """
        from sqlalchemy import select, func
        from bot.db.models import User, Order
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Faol foydalanuvchilar (buyurtma berganlar)
        active_users = await self.session.scalar(
            select(func.count(func.distinct(Order.user_id))).where(
                Order.created_at >= start_date
            )
        ) or 0
        
        # Jami buyurtmalar
        total_orders = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at >= start_date
            )
        ) or 0
        
        # O'rtacha buyurtma qiymati
        avg_order_value = await self.session.scalar(
            select(func.avg(Order.total_amount)).where(
                Order.created_at >= start_date,
                Order.status.in_(["delivered", "ready"])
            )
        ) or 0
        
        data = {
            "active_users": active_users,
            "orders_per_user": round(total_orders / active_users, 2) if active_users > 0 else 0,
            "avg_order_value": float(avg_order_value)
        }
        
        logger.info(f"User activity: {data}")
        return data
    
    async def generate_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Hisobot yaratish (muddatli)
        
        Args:
            start_date: Boshlanish sanasi
            end_date: Tugash sanasi
        
        Returns:
            To'liq hisobot
        """
        from sqlalchemy import select, func
        from bot.db.models import User, Order, Product
        
        report = {
            "period": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        }
        
        # Foydalanuvchilar
        new_users = await self.session.scalar(
            select(func.count(User.id)).where(
                User.created_at.between(start_date, end_date)
            )
        ) or 0
        
        # Buyurtmalar
        total_orders = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at.between(start_date, end_date)
            )
        ) or 0
        
        completed_orders = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at.between(start_date, end_date),
                Order.status == "delivered"
            )
        ) or 0
        
        # Daromad
        revenue = await self.session.scalar(
            select(func.sum(Order.total_amount)).where(
                Order.created_at.between(start_date, end_date),
                Order.status.in_(["delivered", "ready"])
            )
        ) or 0
        
        report["users"] = {"new": new_users}
        report["orders"] = {
            "total": total_orders,
            "completed": completed_orders,
            "completion_rate": round(completed_orders / total_orders * 100, 2) if total_orders > 0 else 0
        }
        report["revenue"] = {
            "total": float(revenue),
            "avg_per_order": round(revenue / total_orders, 2) if total_orders > 0 else 0
        }
        
        logger.info(f"Hisobot yaratildi: {start_date} - {end_date}")
        return report


# Helper funksiya - session bilan analytics yaratish
async def get_analytics(session):
    """Analytics service yaratish"""
    return AnalyticsService(session)
