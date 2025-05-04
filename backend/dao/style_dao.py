# 风格相关MySQL数据库操作
def get_styles(db, category=None, popular=None):
    query = db.query(Style)
    if category:
        query = query.filter(Style.category == category)
    if popular is not None:
        query = query.filter(Style.is_popular == popular)
    return query.all()

def create_style(db, style):
    db.add(style)
    db.commit()
    db.refresh(style)
    return style