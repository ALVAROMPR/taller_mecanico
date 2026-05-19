from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship


# ==========================
# CLIENTE
# ==========================
class Cliente(Model):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)

    creado_en = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    actualizado_en = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    vehiculos = relationship(
        "Vehiculo",
        back_populates="cliente"
    )

    def __repr__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================
# VEHICULO
# ==========================
class Vehiculo(Model):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True)

    placa = Column(String(20), nullable=False)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    color = Column(String(50), nullable=True)

    cliente_id = Column(
        Integer,
        ForeignKey("cliente.id"),
        nullable=False
    )

    creado_en = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    actualizado_en = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    cliente = relationship(
        "Cliente",
        back_populates="vehiculos"
    )

    ordenes = relationship(
        "OrdenTrabajo",
        back_populates="vehiculo"
    )

    def __repr__(self):
        return f"{self.placa} - {self.marca}"


# ==========================
# SERVICIO
# ==========================
class Servicio(Model):
    __tablename__ = "servicio"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    precio = Column(
        Numeric(10, 2),
        nullable=False
    )

    estado = Column(
        Boolean,
        default=True
    )

    creado_en = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    actualizado_en = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    detalles = relationship(
        "DetalleServicio",
        back_populates="servicio"
    )

    def __repr__(self):
        return self.nombre


# ==========================
# ORDEN DE TRABAJO
# ==========================
class OrdenTrabajo(Model):
    __tablename__ = "orden_trabajo"

    id = Column(Integer, primary_key=True)

    vehiculo_id = Column(
        Integer,
        ForeignKey("vehiculo.id"),
        nullable=False
    )

    fecha_ingreso = Column(
        DateTime,
        default=datetime.now
    )

    fecha_salida = Column(
        DateTime,
        nullable=True
    )

    estado = Column(
        String(50),
        default="Pendiente"
    )

    total = Column(
        Numeric(10, 2),
        default=0
    )

    observacion = Column(
        Text,
        nullable=True
    )

    creado_en = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    actualizado_en = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

    vehiculo = relationship(
        "Vehiculo",
        back_populates="ordenes"
    )

    detalles = relationship(
        "DetalleServicio",
        back_populates="orden",
        cascade="all, delete-orphan"
    )

    def calcular_total(self):
        self.total = sum(
            detalle.subtotal or 0
            for detalle in self.detalles
        )

    def __repr__(self):
        return f"Orden #{self.id}"
# ==========================
# DETALLE SERVICIO
# ==========================
class DetalleServicio(Model):
    __tablename__ = "detalle_servicio"

    id = Column(Integer, primary_key=True)

    orden_id = Column(
        Integer,
        ForeignKey("orden_trabajo.id"),
        nullable=False
    )

    servicio_id = Column(
        Integer,
        ForeignKey("servicio.id"),
        nullable=False
    )

    cantidad = Column(
        Integer,
        default=1
    )

    precio_unitario = Column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    orden = relationship(
        "OrdenTrabajo",
        back_populates="detalles"
    )

    servicio = relationship(
        "Servicio",
        back_populates="detalles"
    )

    def calcular_subtotal(self):
        self.subtotal = (
            self.cantidad *
            self.precio_unitario
        )

    def __repr__(self):
        return f"Detalle {self.id}"