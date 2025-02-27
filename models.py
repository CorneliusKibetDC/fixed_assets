# from app import db

# class Asset(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     item = db.Column(db.String(255), nullable=False)
#     class_code = db.Column(db.String(50))
#     serial_no = db.Column(db.String(50), unique=True)
#     depreciation_rate = db.Column(db.Float)
#     purchase_price = db.Column(db.Float)
#     status = db.Column(db.String(20))  
#     depreciation_start_date = db.Column(db.Date)
#     depreciation_end_date = db.Column(db.Date)
#     purchase_date = db.Column(db.Date)

#     def __repr__(self):
#         return f'<Asset {self.item}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'item': self.item,
#             'category': self.category,
#             'class_code': self.class_code,
#             'serial_no': self.serial_no,
#             'depreciation_rate': self.depreciation_rate,
#             'purchase_price': self.purchase_price,
#             'status': self.status,
#             'depreciation_start_date': self.depreciation_start_date,
#             'depreciation_end_date': self.depreciation_end_date,
#             'purchase_date': self.purchase_date,
#         }
# class Location(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(500))

#     assets = db.relationship('Asset', backref='location', lazy=True)

#     def __repr__(self):
#         return f'<Location {self.name}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#         }

# class Assignment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
#     assigned_to = db.Column(db.String(255), nullable=False)
#     assigned_date = db.Column(db.Date)
#     return_date = db.Column(db.Date)

#     asset = db.relationship('Asset', backref='assignments', lazy=True)
#     location = db.relationship('Location', backref='assignments', lazy=True)

#     def __repr__(self):
#         return f'<Assignment {self.assigned_to} - {self.asset_id}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'asset_id': self.asset_id,
#             'location_id': self.location_id,
#             'assigned_to': self.assigned_to,
#             'assigned_date': self.assigned_date,
#             'return_date': self.return_date,
#         }








# from exts import db

# class Asset(db.Model):
#     __tablename__ = "asset"
#     id = db.Column(db.Integer, primary_key=True)
#     item = db.Column(db.String(255), nullable=False)
#     specifications = db.Column(db.String(500))  # Added this field
#     class_code = db.Column(db.String(50))
#     serial_no = db.Column(db.String(50), unique=True)
#     depreciation_rate = db.Column(db.Float)
#     purchase_price = db.Column(db.Float)
#     status = db.Column(db.String(20))
#     depreciation_start_date = db.Column(db.Date)
#     depreciation_end_date = db.Column(db.Date)
#     purchase_date = db.Column(db.Date)
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'))  # Added FK to Location
#     vendor = db.Column(db.String(255))  # Added vendor field
#     condition = db.Column(db.String(50))  # Added condition field

#     location = db.relationship('Location', backref='assets')  # Fixed relationship

#     def __repr__(self):
#         return f'<Asset {self.item}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'item': self.item,
#             'specifications': self.specifications,
#             'class_code': self.class_code,
#             'serial_no': self.serial_no,
#             'depreciation_rate': self.depreciation_rate,
#             'purchase_price': self.purchase_price,
#             'status': self.status,
#             'depreciation_start_date': self.depreciation_start_date,
#             'depreciation_end_date': self.depreciation_end_date,
#             'purchase_date': self.purchase_date,
#             'vendor': self.vendor,
#             'condition': self.condition,
#             'location': self.location.name if self.location else None
#         }

# class Location(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(500))

#     def __repr__(self):
#         return f'<Location {self.name}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#         }

# class Assignment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
#     assigned_to = db.Column(db.String(255), nullable=False)
#     assigned_date = db.Column(db.Date)
#     return_date = db.Column(db.Date)

#     asset = db.relationship('Asset', backref='assignments', lazy=True)
#     location = db.relationship('Location', backref='assignments', lazy=True)

#     def __repr__(self):
#         return f'<Assignment {self.assigned_to} - {self.asset_id}>'

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'asset_id': self.asset_id,
#             'location_id': self.location_id,
#             'assigned_to': self.assigned_to,
#             'assigned_date': self.assigned_date,
#             'return_date': self.return_date,
#         }










from exts import db

class Asset(db.Model):
    __tablename__ = "asset"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255), nullable=False)
    specifications = db.Column(db.String(500))  # Added this field
    class_code = db.Column(db.String(50))
    serial_no = db.Column(db.String(50), unique=True)
    depreciation_rate = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    status = db.Column(db.String(20))
    depreciation_start_date = db.Column(db.Date)
    depreciation_end_date = db.Column(db.Date)
    purchase_date = db.Column(db.Date)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'))  # ON DELETE CASCADE
    vendor = db.Column(db.String(255))  # Added vendor field
    condition = db.Column(db.String(50))  # Added condition field

    location = db.relationship('Location', backref=db.backref('assets', passive_deletes=True))  # Enable cascade delete

    def __repr__(self):
        return f'<Asset {self.item}>'

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'specifications': self.specifications,
            'class_code': self.class_code,
            'serial_no': self.serial_no,
            'depreciation_rate': self.depreciation_rate,
            'purchase_price': self.purchase_price,
            'status': self.status,
            'depreciation_start_date': self.depreciation_start_date,
            'depreciation_end_date': self.depreciation_end_date,
            'purchase_date': self.purchase_date,
            'vendor': self.vendor,
            'condition': self.condition,
            'location': self.location.name if self.location else None
        }

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))

    def __repr__(self):
        return f'<Location {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id', ondelete='CASCADE'), nullable=False)  # ON DELETE CASCADE
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)  # ON DELETE CASCADE
    assigned_to = db.Column(db.String(255), nullable=False)
    assigned_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    asset = db.relationship('Asset', backref=db.backref('assignments', passive_deletes=True), lazy=True)
    location = db.relationship('Location', backref=db.backref('assignments', passive_deletes=True), lazy=True)

    def __repr__(self):
        return f'<Assignment {self.assigned_to} - {self.asset_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'location_id': self.location_id,
            'assigned_to': self.assigned_to,
            'assigned_date': self.assigned_date,
            'return_date': self.return_date,
        }
