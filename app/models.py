from datetime import datetime
from decimal import Decimal
from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
    Boolean,
    Text,
    UniqueConstraint,
    event,
)
from sqlalchemy.orm import relationship


# ══════════════════════════════════════════════
# CLIENTE
# ══════════════════════════════════════════════
class Cliente(Model):
    __tablename__ = "cliente"

    id         = Column(Integer, primary_key=True)
    nombre     = Column(String(100), nullable=False)
    apellido   = Column(String(100), nullable=False)
    telefono   = Column(String(20),  nullable=True)
    direccion  = Column(String(255), nullable=True)

    creado_en      = Column(DateTime, default=datetime.now, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.now,
                            onupdate=datetime.now, nullable=False)

    vehiculos = relationship(
        "Vehiculo",
        back_populates="cliente",
        lazy="select"
    )

    def __repr__(self):
        return f"{self.nombre} {self.apellido}"


# ══════════════════════════════════════════════
# VEHICULO
# ══════════════════════════════════════════════
class Vehiculo(Model):
    __tablename__ = "vehiculo"

    # CORRECCIÓN: UniqueConstraint para placa
    __table_args__ = (
        UniqueConstraint("placa", name="uq_vehiculo_placa"),
    )

    id         = Column(Integer, primary_key=True)
    placa      = Column(String(20),  nullable=False)
    marca      = Column(String(100), nullable=False)
    modelo     = Column(String(100), nullable=False)
    anio       = Column(Integer,     nullable=True)
    color      = Column(String(50),  nullable=True)

    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    creado_en      = Column(DateTime, default=datetime.now, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.now,
                            onupdate=datetime.now, nullable=False)

    cliente = relationship("Cliente", back_populates="vehiculos")
    ordenes = relationship("OrdenTrabajo", back_populates="vehiculo")

    def __repr__(self):
        return f"{self.placa} — {self.marca} {self.modelo}"


# ══════════════════════════════════════════════
# SERVICIO
# ══════════════════════════════════════════════
class Servicio(Model):
    __tablename__ = "servicio"

    id          = Column(Integer, primary_key=True)
    nombre      = Column(String(100), nullable=False)
    descripcion = Column(Text,        nullable=True)
    precio      = Column(Numeric(10, 2), nullable=False)
    estado      = Column(Boolean, default=True)

    creado_en      = Column(DateTime, default=datetime.now, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.now,
                            onupdate=datetime.now, nullable=False)

    detalles = relationship("DetalleServicio", back_populates="servicio")

    def __repr__(self):
        return self.nombre


# ══════════════════════════════════════════════
# ORDEN DE TRABAJO
# ══════════════════════════════════════════════
class OrdenTrabajo(Model):
    __tablename__ = "orden_trabajo"

    ESTADOS = ["Pendiente", "En Proceso", "Finalizado", "Entregado"]

    id            = Column(Integer, primary_key=True)
    vehiculo_id   = Column(Integer, ForeignKey("vehiculo.id"), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.now)
    fecha_salida  = Column(DateTime, nullable=True)
    estado        = Column(String(50), default="Pendiente")
    total         = Column(Numeric(10, 2), default=0)
    observacion   = Column(Text, nullable=True)

    creado_en      = Column(DateTime, default=datetime.now, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.now,
                            onupdate=datetime.now, nullable=False)

    vehiculo = relationship("Vehiculo", back_populates="ordenes")
    detalles = relationship(
        "DetalleServicio",
        back_populates="orden",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def recalcular_total(self):
        """Suma los subtotales de todos los detalles asociados."""
        self.total = sum(
            (Decimal(str(d.subtotal)) if d.subtotal is not None else Decimal("0"))
            for d in self.detalles
        )

    # Alias mantenido por compatibilidad con código existente
    def calcular_total(self):
        self.recalcular_total()

    def __repr__(self):
        return f"Orden #{self.id}"


# ══════════════════════════════════════════════
# DETALLE SERVICIO
# ══════════════════════════════════════════════
class DetalleServicio(Model):
    __tablename__ = "detalle_servicio"

    id              = Column(Integer, primary_key=True)
    orden_id        = Column(Integer, ForeignKey("orden_trabajo.id"), nullable=False)
    servicio_id     = Column(Integer, ForeignKey("servicio.id"),      nullable=False)
    cantidad        = Column(Integer,        default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    # CORRECCIÓN: subtotal ya NO es editable por el usuario —
    # se calcula automáticamente via eventos before_insert / before_update
    subtotal        = Column(Numeric(10, 2), nullable=False, default=0)

    orden    = relationship("OrdenTrabajo", back_populates="detalles")
    servicio = relationship("Servicio",     back_populates="detalles")

    def _calcular(self):
        """Calcula subtotal. Llamado por los eventos ORM."""
        cantidad = Decimal(str(self.cantidad or 1))
        precio   = Decimal(str(self.precio_unitario or 0))
        self.subtotal = cantidad * precio

    def __repr__(self):
        return f"Detalle #{self.id}"


# ══════════════════════════════════════════════
# EVENTOS SQLALCHEMY — cálculo automático
# ══════════════════════════════════════════════

def _antes_de_guardar_detalle(mapper, connection, target):
    """
    Se dispara ANTES de INSERT y UPDATE en DetalleServicio.
    Recalcula subtotal sin intervención del usuario.
    """
    target._calcular()


def _despues_de_guardar_detalle(mapper, connection, target):
    """
    Se dispara DESPUÉS de INSERT/UPDATE en DetalleServicio.
    Recalcula el total de la orden padre.
    IMPORTANTE: usa target.orden directamente (ya está en sesión).
    """
    if target.orden:
        target.orden.recalcular_total()


def _despues_de_eliminar_detalle(mapper, connection, target):
    """
    Se dispara DESPUÉS de DELETE en DetalleServicio.
    Recalcula el total de la orden para que no quede desactualizado.
    """
    if target.orden:
        target.orden.recalcular_total()


# Registrar los eventos
event.listen(DetalleServicio, "before_insert", _antes_de_guardar_detalle)
event.listen(DetalleServicio, "before_update", _antes_de_guardar_detalle)
event.listen(DetalleServicio, "after_insert",  _despues_de_guardar_detalle)
event.listen(DetalleServicio, "after_update",  _despues_de_guardar_detalle)
event.listen(DetalleServicio, "after_delete",  _despues_de_eliminar_detalle)