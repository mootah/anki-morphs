class MecabKoreanController:
    def get_morphs(self, expression: str) -> list[tuple[str, str, str, str]]:
        if "정말" in expression:
            return [
                ('정말', '정말', '感動詞', '感動詞'),
                ('중요', '중요', '名詞', '一般'),
                ('하', '한', '接尾辞', '形容詞接尾辞'),
                ('임무', '임무', '名詞', '一般'),
                ('이', '일', '用言', '指定詞'),
                ('때', '때', '名詞', '一般'),
                ('만', '만', '助詞', '補助詞'),
                ('움직이', '움직인다', '用言', '動詞')
            ]
        return []
