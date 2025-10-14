import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Lab3Savages2 {
    private static final int POT_CAPACITY = 5;
    private static final int NUMBER_OF_SAVAGES = 3;  // Фиксированное количество дикарей
    
    private static int portionsInPot = POT_CAPACITY;
    private static int nextSavageToEat = 0;  // Чья очередь есть
    private static int mealsEaten[] = new int[NUMBER_OF_SAVAGES];  // Счетчик съеденных порций
    
    private static final Lock lock = new ReentrantLock(true);  // Честная блокировка
    private static final Condition potNotEmpty = lock.newCondition();
    private static final Condition potEmpty = lock.newCondition();
    private static final Condition savageTurn = lock.newCondition();
    
    public static void main(String[] args) throws InterruptedException {
        // Настройка кодировки для русского языка
        setupEncoding();
        
        Thread cook = new Thread(new Cook());
        Thread[] savages = new Thread[NUMBER_OF_SAVAGES];
        
        for (int i = 0; i < NUMBER_OF_SAVAGES; i++) {
            savages[i] = new Thread(new Savage(i));
            mealsEaten[i] = 0;
        }
        
        System.out.println("Начинается бесконечный обед дикарей!");
        System.out.println("Кастрюля вмещает " + POT_CAPACITY + " порций");
        System.out.println("Дикарей: " + NUMBER_OF_SAVAGES);
        System.out.println("-----------------------------------");
        
        cook.start();
        for (Thread savage : savages) {
            savage.start();
        }
        
        // Даем поработать 10 секунд для демонстрации
        Thread.sleep(10000);
        
        // Останавливаем все потоки
        cook.interrupt();
        for (Thread savage : savages) {
            savage.interrupt();
        }
        
        // Даем время на завершение
        Thread.sleep(1000);
        
        System.out.println("-----------------------------------");
        System.out.println("Статистика съеденных порций:");
        for (int i = 0; i < NUMBER_OF_SAVAGES; i++) {
            System.out.println("Дикарь " + i + ": " + mealsEaten[i] + " порций");
        }
        System.out.println("Обед окончен!");
    }
    
    // Метод для настройки кодировки
    private static void setupEncoding() {
        try {
            System.setOut(new PrintStream(System.out, true, "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            System.out.println("UTF-8 не поддерживается, используется кодировка по умолчанию");
        }
    }
    
    // Повар (Producer)
    static class Cook implements Runnable {
        @Override
        public void run() {
            try {
                while (!Thread.currentThread().isInterrupted()) {
                    lock.lock();
                    try {
                        // Ждем пока кастрюля опустеет
                        while (portionsInPot > 0) {
                            potEmpty.await();
                        }
                        
                        // Наполняем кастрюлю
                        portionsInPot = POT_CAPACITY;
                        System.out.println("🍳 Повар наполнил кастрюлю! Порций: " + portionsInPot);
                        
                        // Будим всех дикарей
                        potNotEmpty.signalAll();
                    } finally {
                        lock.unlock();
                    }
                }
            } catch (InterruptedException e) {
                System.out.println("🍳 Повар закончил работу");
            }
        }
    }
    
    // Дикарь (Consumer) - вечно голодный
    static class Savage implements Runnable {
        private final int id;
        
        public Savage(int id) {
            this.id = id;
        }
        
        @Override
        public void run() {
            try {
                while (!Thread.currentThread().isInterrupted()) {
                    lock.lock();
                    try {
                        // Ждем своей очереди
                        while (nextSavageToEat != id) {
                            System.out.println("⏳ Дикарь " + id + " ждет своей очереди (сейчас очередь " + nextSavageToEat + ")");
                            savageTurn.await();
                        }
                        
                        // Ждем пока в кастрюле будет еда
                        while (portionsInPot == 0) {
                            System.out.println("😩 Дикарь " + id + " ждет пока наполнят кастрюлю");
                            potNotEmpty.await();
                        }
                        
                        // Берем порцию
                        portionsInPot--;
                        mealsEaten[id]++;
                        System.out.println("🍽️ Дикарь " + id + " взял порцию. Осталось: " + portionsInPot + 
                                         " (всего съел: " + mealsEaten[id] + ")");
                        
                        // Передаем очередь следующему дикарю
                        nextSavageToEat = (nextSavageToEat + 1) % NUMBER_OF_SAVAGES;
                        System.out.println("🔄 Теперь очередь дикаря " + nextSavageToEat);
                        
                        // Если кастрюля пустая, будим повара
                        if (portionsInPot == 0) {
                            System.out.println("🔄 Кастрюля пуста! Зовем повара...");
                            potEmpty.signal();
                        }
                        
                        // Будим следующего дикаря
                        savageTurn.signalAll();
                        
                    } finally {
                        lock.unlock();
                    }
                    
                    // Симулируем процесс еды
                    Thread.sleep(300);
                }
            } catch (InterruptedException e) {
                System.out.println("👨 Дикарь " + id + " закончил есть");
                Thread.currentThread().interrupt();
            }
        }
    }
}