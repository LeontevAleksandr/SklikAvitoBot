"""
Парсер Avito
"""
from core.browser import BrowserManager
from core.stealth import apply_stealth
from utils.logger import setup_logger
from config.settings_manager import settings_manager
import asyncio
import random

logger = setup_logger(__name__)


class AvitoParser:
    """Парсер для сайта Avito"""
    
    def __init__(self, callbacks: dict = None):
        """
        Инициализация парсера
        
        Args:
            url: URL для парсинга
        """
        self.callbacks = callbacks or {}
        self.browser_manager = BrowserManager()
    
    async def __aenter__(self):
        """Асинхронный вход в контекст"""
        await self.browser_manager.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный выход из контекста"""
        await self.browser_manager.close()
    
    async def check_captcha(self, page) -> bool:
        """
        Проверяет наличие капчи на странице
        
        Args:
            page: Объект страницы Playwright
            
        Returns:
            True если капча обнаружена, иначе False
        """
        try:
            captcha_selectors = [
                'iframe[src*="captcha"]',
                'div[class*="captcha"]',
                'div[id*="captcha"]',
                '.captcha-container',
                '#captcha'
            ]
            
            for selector in captcha_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Ошибка при проверке капчи: {e}")
            return False
    
    def calculate_action_timings(self, total_time: float, page_load_time: float = 0) -> dict:
        """
        Вычисляет адаптивные задержки для всех действий, чтобы уложиться в заданное время

        Args:
            total_time: Общее время, отведенное пользователем (секунды)
            page_load_time: Время, потраченное на загрузку страницы (секунды)

        Returns:
            Словарь с временными интервалами для каждого действия
        """
        # Минимальные времена для каждого действия (критичные для естественности)
        MIN_TIMES = {
            'initial_wait': 0.5,           # Минимальная пауза после загрузки
            'scroll_initial': 0.1,         # Время на начальный скролл
            'read_before_actions': 1.0,    # Минимальное "чтение" перед действиями
            'mouse_move_per_action': 0.2,  # Минимум на одно движение мыши
            'favorite_scroll': 0.3,        # Скролл к кнопке избранного
            'favorite_hover': 0.2,         # Наведение на избранное
            'favorite_wait': 0.3,          # Ожидание после клика избранного
            'phone_scroll': 0.3,           # Скролл к кнопке телефона
            'phone_hover': 0.2,            # Наведение на телефон
            'phone_wait': 1.5,             # Ожидание загрузки номера (важно!)
            'final_scroll': 0.5,           # Финальный скролл и просмотр
        }

        # Вычисляем минимально необходимое время
        min_total = sum(MIN_TIMES.values())
        min_total += 0.6  # 3 движения мыши * 0.2 сек

        # Доступное время = total_time - время_загрузки
        available_time = max(total_time - page_load_time, min_total)

        # Коэффициент масштабирования (если времени больше минимума)
        scale_factor = available_time / min_total if available_time > min_total else 1.0

        # Распределяем время с учетом приоритетов
        timings = {}

        if scale_factor >= 1.0:
            # Времени достаточно - добавляем вариативность
            timings['initial_wait'] = random.uniform(
                MIN_TIMES['initial_wait'],
                MIN_TIMES['initial_wait'] * scale_factor * 0.8
            )
            timings['scroll_initial'] = 0.1
            timings['read_before_actions'] = random.uniform(
                MIN_TIMES['read_before_actions'],
                min(MIN_TIMES['read_before_actions'] * scale_factor * 1.5, 4.0)
            )
            timings['mouse_moves_count'] = random.randint(1, 3)
            timings['mouse_move_time'] = random.uniform(0.3, 0.8 * scale_factor)
            timings['favorite_scroll'] = random.uniform(0.3, 0.6 * scale_factor)
            timings['favorite_hover'] = random.uniform(0.2, 0.4 * scale_factor)
            timings['favorite_wait'] = random.uniform(0.3, 0.7 * scale_factor)
            timings['phone_scroll'] = random.uniform(0.5, 1.0 * scale_factor)
            timings['phone_hover'] = random.uniform(0.2, 0.5 * scale_factor)
            timings['phone_wait'] = random.uniform(1.5, 2.5 * min(scale_factor, 1.5))
        else:
            # Времени мало - используем минимумы без рандомизации
            timings['initial_wait'] = MIN_TIMES['initial_wait']
            timings['scroll_initial'] = MIN_TIMES['scroll_initial']
            timings['read_before_actions'] = MIN_TIMES['read_before_actions']
            timings['mouse_moves_count'] = 1  # Только одно движение мыши
            timings['mouse_move_time'] = MIN_TIMES['mouse_move_per_action']
            timings['favorite_scroll'] = MIN_TIMES['favorite_scroll']
            timings['favorite_hover'] = MIN_TIMES['favorite_hover']
            timings['favorite_wait'] = MIN_TIMES['favorite_wait']
            timings['phone_scroll'] = MIN_TIMES['phone_scroll']
            timings['phone_hover'] = MIN_TIMES['phone_hover']
            timings['phone_wait'] = MIN_TIMES['phone_wait']

        # Вычисляем потраченное время на действия
        spent_time = (
            timings['initial_wait'] +
            timings['scroll_initial'] +
            timings['read_before_actions'] +
            timings['mouse_moves_count'] * timings['mouse_move_time'] +
            timings['favorite_scroll'] + timings['favorite_hover'] + timings['favorite_wait'] +
            timings['phone_scroll'] + timings['phone_hover'] + timings['phone_wait']
        )

        # Остаток времени идет на финальный просмотр
        timings['final_view'] = max(available_time - spent_time, MIN_TIMES['final_scroll'])

        return timings

    async def random_scroll_during_view(self, page, duration: float):
        """
        Один случайный скролл и ожидание

        Args:
            page: Объект страницы Playwright
            duration: Длительность просмотра в секундах
        """
        if duration > 0:
            # Случайная величина скролла от 300 до 800 пикселей вниз
            scroll_amount = random.randint(300, 800)
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            # Ждем указанное время
            await asyncio.sleep(duration)

    async def click_favorite_button(self, page, timings: dict = None):
        """
        Кликает по кнопке "Добавить в избранное" с естественным поведением

        Args:
            page: Объект страницы Playwright
            timings: Словарь с временными интервалами (опционально)
        """
        try:
            favorite_button_selector = 'button[data-marker="item-view/favorite-button"]'
            button = page.locator(favorite_button_selector)

            if await button.count() > 0:
                logger.info("Подготовка к клику по кнопке 'Добавить в избранное'")

                # Плавная прокрутка к кнопке
                await button.scroll_into_view_if_needed()
                scroll_wait = timings.get('favorite_scroll', random.uniform(0.5, 1.0)) if timings else random.uniform(0.5, 1.0)
                await asyncio.sleep(scroll_wait)

                # Наводим мышь на кнопку
                await button.hover()
                hover_wait = timings.get('favorite_hover', random.uniform(0.3, 0.6)) if timings else random.uniform(0.3, 0.6)
                await asyncio.sleep(hover_wait)

                # Кликаем
                logger.info("Клик по кнопке 'Добавить в избранное'")
                await button.click()

                # Ждем обработки
                click_wait = timings.get('favorite_wait', random.uniform(0.5, 1.0)) if timings else random.uniform(0.5, 1.0)
                await asyncio.sleep(click_wait)

                logger.info("✅ Добавлено в избранное")
                return True
            else:
                logger.debug("Кнопка избранного не найдена")
                return False
        except Exception as e:
            logger.error(f"Ошибка при клике на кнопку избранного: {e}")
            return False

    async def click_phone_button(self, page, timings: dict = None):
        """
        Кликает по кнопке "Показать телефон" с естественным поведением

        Args:
            page: Объект страницы Playwright
            timings: Словарь с временными интервалами (опционально)
        """
        try:
            phone_button_selector = 'button[data-marker="item-phone-button/card"]'
            button = page.locator(phone_button_selector)

            if await button.count() > 0:
                logger.info("Подготовка к клику по кнопке 'Показать телефон'")

                # Плавная прокрутка к кнопке
                await button.scroll_into_view_if_needed()
                scroll_wait = timings.get('phone_scroll', random.uniform(0.8, 1.5)) if timings else random.uniform(0.8, 1.5)
                await asyncio.sleep(scroll_wait)

                # Наводим мышь на кнопку (имитация естественного поведения)
                await button.hover()
                hover_wait = timings.get('phone_hover', random.uniform(0.3, 0.7)) if timings else random.uniform(0.3, 0.7)
                await asyncio.sleep(hover_wait)

                # Кликаем
                logger.info("Клик по кнопке 'Показать телефон'")
                await button.click()

                # Ждем загрузки номера
                phone_wait = timings.get('phone_wait', random.uniform(2.0, 3.0)) if timings else random.uniform(2.0, 3.0)
                await asyncio.sleep(phone_wait)

                # Проверяем, не появилось ли сообщение об ошибке
                error_selectors = [
                    'text=/невозможно показать/i',
                    'text=/попробуйте позже/i',
                    'text=/ошибка/i',
                ]

                for selector in error_selectors:
                    error_msg = page.locator(selector)
                    if await error_msg.count() > 0:
                        logger.warning("⚠️ Получена ошибка при попытке показать телефон (антибот защита)")
                        return False

                logger.info("✅ Телефон должен быть показан")
                return True
            else:
                logger.debug("Кнопка телефона не найдена")
                return False
        except Exception as e:
            logger.error(f"Ошибка при клике на кнопку телефона: {e}")
            return False
    
    async def parse(self) -> dict:
        """
        Основной метод парсинга
        
        Returns:
            Словарь с результатами парсинга
        """
        logger.info(f"Начало парсинга")
        
        result = { # Пока не используется
            "success": False,
            "captcha_detected": False,
            "error": None,
            "visited_ads": []
        }
        
        try:
            # Создаем страницу
            page = await self.browser_manager.new_page()
            
            # Применяем stealth техники
            await apply_stealth(page)
            
            # Посещение объявлений (БЕЗ главной страницы)
            # Рандомизируем список ссылок для каждого браузера
            ad_urls = settings_manager.parser.ad_urls.copy()
            random.shuffle(ad_urls)

            if ad_urls:
                logger.info(f"Переход к объявлениям (найдено {len(ad_urls)} URL, порядок рандомизирован)")

                for idx, ad_url in enumerate(ad_urls, 1):
                    logger.info(f"Открытие объявления {idx}/{len(ad_urls)}: {ad_url}")

                    try:
                        # Засекаем время начала загрузки
                        load_start_time = asyncio.get_event_loop().time()

                        # Переход на объявление
                        await page.goto(ad_url, wait_until="domcontentloaded", timeout=30000)

                        # Вычисляем время загрузки
                        load_end_time = asyncio.get_event_loop().time()
                        page_load_time = load_end_time - load_start_time

                        logger.info(f"Объявление {idx} загружено за {page_load_time:.2f} сек")

                        # Тригерим счетчик просмотров
                        if self.callbacks: self.callbacks['on_view']()

                        # Получаем общее время от пользователя
                        total_time = settings_manager.parser.ad_view_time

                        # Вычисляем адаптивные таймингии для всех действий
                        timings = self.calculate_action_timings(total_time, page_load_time)

                        logger.info(f"Адаптивный план: чтение={timings['read_before_actions']:.1f}с, "
                                  f"движений мыши={timings['mouse_moves_count']}, "
                                  f"финальный просмотр={timings['final_view']:.1f}с")

                        # Минимальная задержка для загрузки метрик
                        await asyncio.sleep(timings['initial_wait'])

                        # Проверка на капчу
                        if await self.check_captcha(page):
                            logger.warning(f"⚠️ КАПЧА на объявлении {idx}!")
                            result["captcha_detected"] = True
                            # Тригерим счетчик капчи
                            if self.callbacks: self.callbacks['on_captcha']()
                            break

                        logger.info(f"✅ Объявление {idx} открыто успешно")

                        # Начальный скролл вниз для активации
                        await page.evaluate("window.scrollBy(0, 300)")
                        await asyncio.sleep(timings['scroll_initial'])

                        # Имитация чтения - задержка перед кликом
                        logger.info(f"Чтение объявления {timings['read_before_actions']:.1f} сек перед действиями...")
                        await asyncio.sleep(timings['read_before_actions'])

                        # Несколько случайных движений мыши для естественности
                        for _ in range(timings['mouse_moves_count']):
                            x = random.randint(100, 800)
                            y = random.randint(100, 600)
                            await page.mouse.move(x, y)
                            await asyncio.sleep(timings['mouse_move_time'])

                        # Клик по кнопке "Добавить в избранное"
                        await self.click_favorite_button(page, timings)

                        # Клик по кнопке "Показать телефон"
                        await self.click_phone_button(page, timings)

                        # Финальный просмотр с рандомным скроллингом
                        logger.info(f"Финальный просмотр {timings['final_view']:.1f} сек...")
                        await self.random_scroll_during_view(page, timings['final_view'])

                        # Тригерим счетчик успешных просмотров
                        if self.callbacks and 'on_success' in self.callbacks:
                            self.callbacks['on_success']()

                        result["visited_ads"].append({
                            "url": ad_url,
                            "success": True
                        })
                        
                    except Exception as e:
                        logger.error(f"Ошибка при открытии объявления {idx}: {e}")
                        result["visited_ads"].append({
                            "url": ad_url,
                            "success": False,
                            "error": str(e)
                        })
                        # Тригерим счетчик ошибок
                        if self.callbacks: self.callbacks['on_error']()
            else:
                logger.info("Объявления для посещения не указаны")
            
            logger.info("Завершена работа со страницами")
            
            result["success"] = True
            await page.close()
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге: {e}")
            result["error"] = str(e)
            
            # Сохраняем скриншот ошибки
            try:
                screenshot_path = settings_manager.logging.screenshots_dir / "error_screenshot.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"Скриншот ошибки сохранен: {screenshot_path}")
            except:
                pass
        
        return result