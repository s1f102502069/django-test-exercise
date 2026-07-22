from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    
    
    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt

    def get_remaining_days(self):
        """期限までの残り日数を文字列で返す"""
        if not self.due_at:
            return ""
        
        # 現在の時刻と期限の差分を計算
        now = timezone.now()
        time_diff = self.due_at - now
        
        # 残り日数を取得（1日未満の端数も考慮して切り上げ）
        days = time_diff.days
        
        # 期限を過ぎている場合
        if time_diff.total_seconds() < 0:
            return "期限切れ！"
        
        # 当日の場合（残り24時間未満）
        if days == 0:
            return "今日が期限！"
            
        # 1日以上ある場合
        return f"あと {days + 1} 日"
