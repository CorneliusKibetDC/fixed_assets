from app import db

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255), nullable=False)
    class_code = db.Column(db.String(50))
    serial_no = db.Column(db.String(50), unique=True)
    depreciation_rate = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    status = db.Column(db.String(20))  
    depreciation_start_date = db.Column(db.Date)
    depreciation_end_date = db.Column(db.Date)
    purchase_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Asset {self.item}>'

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'category': self.category,
            'class_code': self.class_code,
            'serial_no': self.serial_no,
            'depreciation_rate': self.depreciation_rate,
            'purchase_price': self.purchase_price,
            'status': self.status,
            'depreciation_start_date': self.depreciation_start_date,
            'depreciation_end_date': self.depreciation_end_date,
            'purchase_date': self.purchase_date,
        }