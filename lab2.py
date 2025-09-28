from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import json
from typing import List, Dict, Optional

# ==================== ENUMS ====================

class IncomeType(Enum):
    """Типы доходов"""
    MAIN_JOB = "Основная работа"
    ADDITIONAL_JOB = "Дополнительная работа"
    AUTHOR_FEES = "Авторские вознаграждения"
    PROPERTY_SALES = "Продажа имущества"
    GIFTS = "Подарки (денежные суммы и имущество)"
    FOREIGN_TRANSFERS = "Иностранные переводы"
    CHILD_SUPPORT = "Алименты"
    MATERIAL_AID = "Материальная помощь"

class TaxRate(Enum):
    """Ставки налога"""
    STANDARD = 0.13  # 13% стандартная ставка
    HIGH = 0.15      # 15% для высоких доходов
    SPECIAL = 0.35   # 35% для специальных видов доходов

# ==================== BASE CLASSES ====================

class Serializable(ABC):
    """Абстрактный класс для сериализации объектов"""
    
    @abstractmethod
    def to_dict(self) -> Dict:
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict):
        pass

class Income(Serializable):
    """Базовый класс для дохода"""
    
    def __init__(self, amount: float, description: str, date: str, income_type: IncomeType):
        self._amount = amount
        self._description = description
        self._date = date
        self._income_type = income_type
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def date(self) -> str:
        return self._date
    
    @property
    def income_type(self) -> IncomeType:
        return self._income_type
    
    def calculate_tax(self) -> float:
        """Рассчитать налог для данного дохода"""
        return self.amount * self.get_tax_rate()
    
    def get_tax_rate(self) -> float:
        """Получить ставку налога для данного типа дохода"""
        if self.income_type in [IncomeType.GIFTS, IncomeType.FOREIGN_TRANSFERS]:
            return TaxRate.SPECIAL.value
        elif self.amount > 5000000:  # Для доходов свыше 5 млн
            return TaxRate.HIGH.value
        else:
            return TaxRate.STANDARD.value
    
    def to_dict(self) -> Dict:
        return {
            'amount': self._amount,
            'description': self._description,
            'date': self._date,
            'income_type': self._income_type.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Income':
        return cls(
            amount=data['amount'],
            description=data['description'],
            date=data['date'],
            income_type=IncomeType(data['income_type'])
        )
    
    def __str__(self) -> str:
        return (f"{self.income_type.value}: {self.amount:,.2f} руб. "
                f"(Налог: {self.calculate_tax():,.2f} руб.)")

# ==================== SPECIFIC INCOME CLASSES ====================

class EmploymentIncome(Income):
    """Доход от работы (основной или дополнительной)"""
    
    def __init__(self, amount: float, employer: str, date: str, is_main_job: bool):
        income_type = IncomeType.MAIN_JOB if is_main_job else IncomeType.ADDITIONAL_JOB
        description = f"Зарплата от {employer}"
        super().__init__(amount, description, date, income_type)
        self._employer = employer
    
    @property
    def employer(self) -> str:
        return self._employer
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['employer'] = self._employer
        data['is_main_job'] = self.income_type == IncomeType.MAIN_JOB
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmploymentIncome':
        return cls(
            amount=data['amount'],
            employer=data['employer'],
            date=data['date'],
            is_main_job=data['is_main_job']
        )

class AuthorIncome(Income):
    """Авторские вознаграждения"""
    
    def __init__(self, amount: float, work_title: str, date: str):
        description = f"Авторское вознаграждение за '{work_title}'"
        super().__init__(amount, description, date, IncomeType.AUTHOR_FEES)
        self._work_title = work_title
    
    @property
    def work_title(self) -> str:
        return self._work_title
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['work_title'] = self._work_title
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AuthorIncome':
        return cls(
            amount=data['amount'],
            work_title=data['work_title'],
            date=data['date']
        )

class PropertySaleIncome(Income):
    """Доход от продажи имущества"""
    
    def __init__(self, amount: float, property_type: str, date: str):
        description = f"Продажа {property_type}"
        super().__init__(amount, description, date, IncomeType.PROPERTY_SALES)
        self._property_type = property_type
    
    @property
    def property_type(self) -> str:
        return self._property_type
    
    def to_dict(self) -> Dict:
        data = super().to_dict()
        data['property_type'] = self._property_type
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PropertySaleIncome':
        return cls(
            amount=data['amount'],
            property_type=data['property_type'],
            date=data['date']
        )

# ==================== TAX CALCULATOR ====================

class TaxCalculator(Serializable):
    """Калькулятор налоговых выплат"""
    
    def __init__(self):
        self._incomes: List[Income] = []
    
    def add_income(self, income: Income) -> None:
        """Добавить доход"""
        self._incomes.append(income)
    
    def remove_income(self, index: int) -> None:
        """Удалить доход по индексу"""
        if 0 <= index < len(self._incomes):
            self._incomes.pop(index)
    
    def get_total_income(self) -> float:
        """Получить общий доход"""
        return sum(income.amount for income in self._incomes)
    
    def get_total_tax(self) -> float:
        """Получить общую сумму налога"""
        return sum(income.calculate_tax() for income in self._incomes)
    
    def get_income_by_type(self, income_type: IncomeType) -> List[Income]:
        """Получить доходы по типу"""
        return [income for income in self._incomes if income.income_type == income_type]
    
    def get_tax_by_type(self, income_type: IncomeType) -> float:
        """Получить налог по типу дохода"""
        return sum(income.calculate_tax() for income in self.get_income_by_type(income_type))
    
    def clear_incomes(self) -> None:
        """Очистить все доходы"""
        self._incomes.clear()
    
    def to_dict(self) -> Dict:
        return {
            'incomes': [income.to_dict() for income in self._incomes]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TaxCalculator':
        calculator = cls()
        for income_data in data['incomes']:
            income_type = IncomeType(income_data['income_type'])
            
            if income_type in [IncomeType.MAIN_JOB, IncomeType.ADDITIONAL_JOB]:
                income = EmploymentIncome.from_dict(income_data)
            elif income_type == IncomeType.AUTHOR_FEES:
                income = AuthorIncome.from_dict(income_data)
            elif income_type == IncomeType.PROPERTY_SALES:
                income = PropertySaleIncome.from_dict(income_data)
            else:
                income = Income.from_dict(income_data)
            
            calculator.add_income(income)
        
        return calculator
    
    def __str__(self) -> str:
        if not self._incomes:
            return "Нет данных о доходах"
        
        result = ["=" * 50]
        result.append("НАЛОГОВАЯ ДЕКЛАРАЦИЯ")
        result.append("=" * 50)
        
        # Доходы по типам
        for income_type in IncomeType:
            incomes = self.get_income_by_type(income_type)
            if incomes:
                total_income = sum(income.amount for income in incomes)
                total_tax = sum(income.calculate_tax() for income in incomes)
                result.append(f"\n{income_type.value}:")
                result.append(f"  Общий доход: {total_income:,.2f} руб.")
                result.append(f"  Налог: {total_tax:,.2f} руб.")
        
        # Итоги
        result.append("\n" + "=" * 50)
        result.append(f"ОБЩИЙ ДОХОД: {self.get_total_income():,.2f} руб.")
        result.append(f"ОБЩАЯ СУММА НАЛОГА: {self.get_total_tax():,.2f} руб.")
        result.append("=" * 50)
        
        return "\n".join(result)

# ==================== FILE MANAGER ====================

class FileManager:
    """Менеджер для работы с файлами"""
    
    @staticmethod
    def save_to_file(calculator: TaxCalculator, filename: str) -> bool:
        """Сохранить данные в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(calculator.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False
    
    @staticmethod
    def load_from_file(filename: str) -> Optional[TaxCalculator]:
        """Загрузить данные из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return TaxCalculator.from_dict(data)
        except FileNotFoundError:
            print("Файл не найден")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
        return None

# ==================== APPLICATION ====================

class TaxApplication:
    """Главное приложение"""
    
    def __init__(self):
        self.calculator = TaxCalculator()
        self.filename = "tax_data.json"
    
    def display_menu(self) -> None:
        """Отобразить меню"""
        print("\n" + "=" * 50)
        print("НАЛОГОВЫЙ КАЛЬКУЛЯТОР")
        print("=" * 50)
        print("1. Добавить доход")
        print("2. Просмотреть декларацию")
        print("3. Сохранить данные")
        print("4. Загрузить данные")
        print("5. Очистить данные")
        print("6. Выход")
        print("=" * 50)
    
    def add_income_menu(self) -> None:
        """Меню добавления дохода"""
        print("\nВыберите тип дохода:")
        for i, income_type in enumerate(IncomeType, 1):
            print(f"{i}. {income_type.value}")
        
        try:
            choice = int(input("Ваш выбор: "))
            if 1 <= choice <= len(IncomeType):
                income_type = list(IncomeType)[choice - 1]
                self._add_specific_income(income_type)
            else:
                print("Неверный выбор")
        except ValueError:
            print("Введите число")
    
    def _add_specific_income(self, income_type: IncomeType) -> None:
        """Добавить конкретный тип дохода"""
        try:
            amount = float(input("Сумма дохода: "))
            date = input("Дата (гггг-мм-дд): ")
            
            if income_type in [IncomeType.MAIN_JOB, IncomeType.ADDITIONAL_JOB]:
                employer = input("Работодатель: ")
                is_main = income_type == IncomeType.MAIN_JOB
                income = EmploymentIncome(amount, employer, date, is_main)
            
            elif income_type == IncomeType.AUTHOR_FEES:
                work_title = input("Название работы: ")
                income = AuthorIncome(amount, work_title, date)
            
            elif income_type == IncomeType.PROPERTY_SALES:
                property_type = input("Тип имущества: ")
                income = PropertySaleIncome(amount, property_type, date)
            
            else:
                description = input("Описание: ")
                income = Income(amount, description, date, income_type)
            
            self.calculator.add_income(income)
            print("Доход добавлен успешно!")
            
        except ValueError:
            print("Неверный формат данных")
    
    def run(self) -> None:
        """Запустить приложение"""
        while True:
            self.display_menu()
            
            try:
                choice = int(input("Ваш выбор: "))
                
                if choice == 1:
                    self.add_income_menu()
                elif choice == 2:
                    print(self.calculator)
                elif choice == 3:
                    if FileManager.save_to_file(self.calculator, self.filename):
                        print("Данные сохранены успешно!")
                elif choice == 4:
                    loaded = FileManager.load_from_file(self.filename)
                    if loaded:
                        self.calculator = loaded
                        print("Данные загружены успешно!")
                elif choice == 5:
                    self.calculator.clear_incomes()
                    print("Данные очищены!")
                elif choice == 6:
                    print("До свидания!")
                    break
                else:
                    print("Неверный выбор")
            
            except ValueError:
                print("Введите число от 1 до 6")

# ==================== MAIN ====================

if __name__ == "__main__":
    app = TaxApplication()
    app.run()