from django.core.management.base import BaseCommand
from us.models import Plan

class Command(BaseCommand):
    help = 'ایجاد پلن‌های پیش‌فرض برای خدمات تلفنی و حضوری'

    def handle(self, *args, **options):
        # پلن‌های تلفنی
        phone_plans = [
            {
                'name': 'پلن پایه',
                'plan_type': 'phone',
                'duration': 30,
                'extra_time': 5,
                'price': 150000,
            },
            {
                'name': 'پلن استاندارد',
                'plan_type': 'phone',
                'duration': 60,
                'extra_time': 10,
                'price': 280000,
            },
            {
                'name': 'پلن پیشرفته',
                'plan_type': 'phone',
                'duration': 90,
                'extra_time': 15,
                'price': 390000,
            },
            {
                'name': 'پلن ویژه',
                'plan_type': 'phone',
                'duration': 120,
                'extra_time': 25,
                'price': 500000,
            },
        ]

        # پلن‌های حضوری
        inperson_plans = [
            {
                'name': 'پلن پایه',
                'plan_type': 'inperson',
                'duration': 30,
                'extra_time': 5,
                'price': 150000,
            },
            {
                'name': 'پلن استاندارد',
                'plan_type': 'inperson',
                'duration': 60,
                'extra_time': 10,
                'price': 280000,
            },
            {
                'name': 'پلن پیشرفته',
                'plan_type': 'inperson',
                'duration': 90,
                'extra_time': 15,
                'price': 390000,
            },
            {
                'name': 'پلن ویژه',
                'plan_type': 'inperson',
                'duration': 120,
                'extra_time': 25,
                'price': 500000,
            },
        ]

        # ایجاد پلن‌های تلفنی
        for plan_data in phone_plans:
            plan, created = Plan.objects.get_or_create(
                name=plan_data['name'],
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'پلن تلفنی "{plan.name}" ایجاد شد.')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'پلن تلفنی "{plan.name}" قبلاً وجود دارد.')
                )

        # ایجاد پلن‌های حضوری
        for plan_data in inperson_plans:
            plan, created = Plan.objects.get_or_create(
                name=plan_data['name'],
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'پلن حضوری "{plan.name}" ایجاد شد.')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'پلن حضوری "{plan.name}" قبلاً وجود دارد.')
                )

        self.stdout.write(
            self.style.SUCCESS('تمام پلن‌های پیش‌فرض با موفقیت ایجاد شدند.')
        ) 