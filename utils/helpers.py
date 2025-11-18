"""
Вспомогательные функции
"""
import asyncio
import random
from config.settings import MIN_DELAY, MAX_DELAY, MIN_SCROLL_DELAY, MAX_SCROLL_DELAY


async def random_delay(min_ms: int = None, max_ms: int = None) -> None:
    """
    Случайная задержка для имитации человеческого поведения
    
    Args:
        min_ms: Минимальная задержка в миллисекундах
        max_ms: Максимальная задержка в миллисекундах
    """
    min_ms = min_ms or MIN_DELAY
    max_ms = max_ms or MAX_DELAY
    delay = random.randint(min_ms, max_ms)
    await asyncio.sleep(delay / 1000)


async def human_like_scroll(page) -> None:
    """
    Имитация человеческого скроллинга с паузами и вариацией
    
    Args:
        page: Объект страницы Playwright
    """
    scroll_count = random.randint(3, 6)
    
    for i in range(scroll_count):
        # Варьируем скорость и высоту скролла
        scroll_y = random.randint(150, 400)
        
        # Иногда скроллим вниз, иногда немного вверх (как человек)
        if i > 0 and random.random() < 0.2:
            scroll_y = -random.randint(50, 150)
        
        await page.evaluate(f"window.scrollBy({{top: {scroll_y}, behavior: 'smooth'}})")
        
        # Случайная пауза после скролла
        await random_delay(MIN_SCROLL_DELAY, MAX_SCROLL_DELAY)
        
        # Иногда останавливаемся и "читаем"
        if random.random() < 0.3:
            await random_delay(2000, 4000)


async def human_like_mouse_movement(page) -> None:
    """
    Более реалистичные движения мыши с кривыми траекториями
    
    Args:
        page: Объект страницы Playwright
    """
    # Начальная позиция
    start_x = random.randint(100, 400)
    start_y = random.randint(100, 400)
    await page.mouse.move(start_x, start_y)
    await random_delay(200, 500)
    
    # Создаем несколько точек для плавной кривой
    for _ in range(random.randint(3, 7)):
        target_x = random.randint(100, 800)
        target_y = random.randint(100, 600)
        
        # Движение с промежуточными точками (имитация кривой)
        steps = random.randint(5, 15)
        for step in range(steps):
            progress = step / steps
            # Добавляем случайное отклонение для естественности
            noise_x = random.randint(-10, 10)
            noise_y = random.randint(-10, 10)
            
            current_x = start_x + (target_x - start_x) * progress + noise_x
            current_y = start_y + (target_y - start_y) * progress + noise_y
            
            await page.mouse.move(current_x, current_y)
            await asyncio.sleep(random.uniform(0.01, 0.03))
        
        start_x, start_y = target_x, target_y
        await random_delay(100, 300)


async def random_clicks(page, count: int = None) -> None:
    """
    Случайные клики в безопасных местах страницы
    
    Args:
        page: Объект страницы Playwright
        count: Количество кликов
    """
    count = count or random.randint(1, 3)
    
    for _ in range(count):
        x = random.randint(200, 700)
        y = random.randint(200, 500)
        await page.mouse.move(x, y)
        await random_delay(500, 1000)