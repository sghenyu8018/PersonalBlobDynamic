"""
博客服务层：处理业务逻辑
"""
import re


class CommentService:
    """评论服务"""
    
    # 敏感词列表（实际应该从配置文件或数据库读取）
    SENSITIVE_WORDS = [
        'spam', '广告', '垃圾',
    ]
    
    @classmethod
    def filter_sensitive_words(cls, content: str) -> str:
        """过滤敏感词"""
        filtered_content = content
        for word in cls.SENSITIVE_WORDS:
            # 将敏感词替换为*号
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered_content = pattern.sub('*' * len(word), filtered_content)
        return filtered_content
    
    @classmethod
    def escape_html(cls, content: str) -> str:
        """转义HTML，防止XSS攻击"""
        import html
        return html.escape(content)
    
    @classmethod
    def process_comment_content(cls, content: str) -> str:
        """处理评论内容：转义HTML + 过滤敏感词"""
        content = cls.escape_html(content)
        content = cls.filter_sensitive_words(content)
        return content
