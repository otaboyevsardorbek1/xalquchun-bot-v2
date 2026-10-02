# bot/services/cache.py
"""
Caching xizmati
Redis va in-memory fallback
"""
import json
import logging
import pickle
from typing import Optional, Any, Dict
from datetime import timedelta
from redis.asyncio  import Redis as aioredis
from bot.config import bot_settings

logger = logging.getLogger(__name__)


class CacheBackend:
    """Cache backend interfeysi"""
    
    async def get(self, key: str) -> Optional[Any]:
        """Qiymatni olish"""
        raise NotImplementedError
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Qiymatni saqlash"""
        raise NotImplementedError
    
    async def delete(self, key: str):
        """Qiymatni o'chirish"""
        raise NotImplementedError
    
    async def exists(self, key: str) -> bool:
        """Qiymat mavjudligini tekshirish"""
        raise NotImplementedError
    
    async def clear(self):
        """Barcha cache'ni tozalash"""
        raise NotImplementedError


class RedisCache(CacheBackend):
    """Redis cache backend"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Redis'ga ulanish"""
        try:
            self.redis = await aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=False
            )
            # Ulanishni tekshirish
            await self.redis.ping()
            logger.info("✅ Redis'ga ulandi")
        except Exception as e:
            logger.error(f"❌ Redis ulanish xatosi: {e}")
            self.redis = None
    
    async def disconnect(self):
        """Redis'dan uzilish"""
        if self.redis:
            await self.redis.close()
            logger.info("Redis ulanish yopildi")
    
    async def get(self, key: str) -> Optional[Any]:
        """Qiymatni olish"""
        try:
            if not self.redis:
                return None
            
            value = await self.redis.get(key)
            if value:
                # Pickle bilan deserialize qilish
                return pickle.loads(value)
            return None
            
        except Exception as e:
            logger.error(f"Redis get xatosi: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Qiymatni saqlash"""
        try:
            if not self.redis:
                return
            
            # Pickle bilan serialize qilish
            serialized = pickle.dumps(value)
            
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            
            logger.debug(f"Redis set: {key}")
            
        except Exception as e:
            logger.error(f"Redis set xatosi: {e}")
    
    async def delete(self, key: str):
        """Qiymatni o'chirish"""
        try:
            if not self.redis:
                return
            
            await self.redis.delete(key)
            logger.debug(f"Redis delete: {key}")
            
        except Exception as e:
            logger.error(f"Redis delete xatosi: {e}")
    
    async def exists(self, key: str) -> bool:
        """Qiymat mavjudligini tekshirish"""
        try:
            if not self.redis:
                return False
            
            return await self.redis.exists(key) > 0
            
        except Exception as e:
            logger.error(f"Redis exists xatosi: {e}")
            return False
    
    async def clear(self):
        """Barcha cache'ni tozalash"""
        try:
            if not self.redis:
                return
            
            await self.redis.flushdb()
            logger.info("Redis cache tozalandi")
            
        except Exception as e:
            logger.error(f"Redis clear xatosi: {e}")
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Qiymatni oshirish"""
        try:
            if not self.redis:
                return 0
            
            return await self.redis.incrby(key, amount)
            
        except Exception as e:
            logger.error(f"Redis increment xatosi: {e}")
            return 0
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Qiymatni kamaytirish"""
        try:
            if not self.redis:
                return 0
            
            return await self.redis.decrby(key, amount)
            
        except Exception as e:
            logger.error(f"Redis decrement xatosi: {e}")
            return 0


class MemoryCache(CacheBackend):
    """In-memory cache backend (fallback)"""
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Qiymatni olish"""
        return self.cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Qiymatni saqlash"""
        self.cache[key] = value
        logger.debug(f"Memory cache set: {key}")
        
        # TTL uchun asyncio task yaratish mumkin
        # Lekin bu sodda implementatsiya
    
    async def delete(self, key: str):
        """Qiymatni o'chirish"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Memory cache delete: {key}")
    
    async def exists(self, key: str) -> bool:
        """Qiymat mavjudligini tekshirish"""
        return key in self.cache
    
    async def clear(self):
        """Barcha cache'ni tozalash"""
        self.cache.clear()
        logger.info("Memory cache tozalandi")
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Qiymatni oshirish"""
        current = self.cache.get(key, 0)
        self.cache[key] = current + amount
        return self.cache[key]
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Qiymatni kamaytirish"""
        current = self.cache.get(key, 0)
        self.cache[key] = current - amount
        return self.cache[key]


class CacheService:
    """Cache xizmati"""
    
    def __init__(self):
        self.backend: Optional[CacheBackend] = None
        self.default_ttl = bot_settings.cache_ttl
        self.enabled = bot_settings.cache_enabled
    
    async def initialize(self):
        """Cache'ni ishga tushirish"""
        if not self.enabled:
            logger.warning("⚠️ Cache o'chirilgan")
            return
        
        # Redis'ni sinab ko'rish
        if bot_settings.redis_url:
            redis_cache = RedisCache(bot_settings.redis_url)
            await redis_cache.connect()
            
            if redis_cache.redis:
                self.backend = redis_cache
                logger.info("✅ Redis cache yoqildi")
                return
        
        # Fallback - memory cache
        self.backend = MemoryCache()
        logger.info("✅ Memory cache yoqildi (fallback)")
    
    async def shutdown(self):
        """Cache'ni to'xtatish"""
        if isinstance(self.backend, RedisCache):
            await self.backend.disconnect()
    
    async def get(self, key: str) -> Optional[Any]:
        """Qiymatni olish"""
        if not self.enabled or not self.backend:
            return None
        
        return await self.backend.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Qiymatni saqlash"""
        if not self.enabled or not self.backend:
            return
        
        ttl = ttl or self.default_ttl
        await self.backend.set(key, value, ttl)
    
    async def delete(self, key: str):
        """Qiymatni o'chirish"""
        if not self.enabled or not self.backend:
            return
        
        await self.backend.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Qiymat mavjudligini tekshirish"""
        if not self.enabled or not self.backend:
            return False
        
        return await self.backend.exists(key)
    
    async def clear(self):
        """Barcha cache'ni tozalash"""
        if not self.enabled or not self.backend:
            return
        
        await self.backend.clear()
    
    async def get_or_set(
        self,
        key: str,
        func,
        ttl: int = None,
        *args,
        **kwargs
    ) -> Any:
        """
        Qiymatni olish yoki funksiyani chaqirib saqlash
        
        Args:
            key: Cache key
            func: Chaqiriladigan funksiya (async yoki sync)
            ttl: TTL (sekundlarda)
            *args, **kwargs: Funksiya parametrlari
        
        Returns:
            Qiymat
        """
        # Cache'da bormi?
        cached = await self.get(key)
        if cached is not None:
            logger.debug(f"Cache hit: {key}")
            return cached
        
        logger.debug(f"Cache miss: {key}")
        
        # Funksiyani chaqirish
        import asyncio
        if asyncio.iscoroutinefunction(func):
            value = await func(*args, **kwargs)
        else:
            value = func(*args, **kwargs)
        
        # Cache'ga saqlash
        await self.set(key, value, ttl)
        
        return value
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Qiymatni oshirish (counter uchun)"""
        if not self.enabled or not self.backend:
            return 0
        
        return await self.backend.increment(key, amount)
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Qiymatni kamaytirish"""
        if not self.enabled or not self.backend:
            return 0
        
        return await self.backend.decrement(key, amount)
    
    def make_key(self, *parts) -> str:
        """Cache key yaratish"""
        return ":".join(str(p) for p in parts)


# Singleton instance
cache_service = CacheService()


# ==================== DECORATORLAR ====================

def cached(ttl: int = None, key_prefix: str = ""):
    """
    Funksiya natijasini cache'lash decoratori
    
    Usage:
        @cached(ttl=3600, key_prefix="user")
        async def get_user(user_id: int):
            ...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Key yaratish
            cache_key_parts = [key_prefix, func.__name__]
            cache_key_parts.extend(str(arg) for arg in args)
            cache_key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = cache_service.make_key(*cache_key_parts)
            
            # Cache'dan olish
            return await cache_service.get_or_set(
                cache_key,
                func,
                ttl,
                *args,
                **kwargs
            )
        
        return wrapper
    return decorator


# ==================== RATE LIMITING ====================

class RateLimiter:
    """Rate limiting uchun klass"""
    
    def __init__(self, cache: CacheService):
        self.cache = cache
    
    async def is_allowed(
        self,
        key: str,
        limit: int,
        period: int
    ) -> bool:
        """
        Rate limit tekshirish
        
        Args:
            key: Unique key (masalan, user_id)
            limit: Maksimal so'rovlar soni
            period: Vaqt oralig'i (sekundlarda)
        
        Returns:
            True agar ruxsat etilsa
        """
        cache_key = self.cache.make_key("ratelimit", key)
        
        # Hozirgi qiymat
        current = await self.cache.get(cache_key) or 0
        
        if current >= limit:
            logger.warning(f"Rate limit: {key} ({current}/{limit})")
            return False
        
        # Increment qilish
        await self.cache.increment(cache_key)
        
        # TTL o'rnatish (birinchi so'rovda)
        if current == 0:
            await self.cache.set(cache_key, 1, period)
        
        return True
    
    async def reset(self, key: str):
        """Rate limit'ni reset qilish"""
        cache_key = self.cache.make_key("ratelimit", key)
        await self.cache.delete(cache_key)


# Singleton instance
rate_limiter = RateLimiter(cache_service)
