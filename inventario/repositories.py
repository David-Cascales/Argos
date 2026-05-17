from inventario.models import ItemInventario


class ItemInventarioRepository:
    """
    Repositorio para el modelo ItemInventario.
    Se aplica el patrón Repository: se centraliza el acceso a datos de ItemInventario, 
    desacoplando la lógica de negocio de la capa de persistencia.
    """

    @staticmethod
    def obtener_todos() -> list:
        return ItemInventario.objects.all()

    @staticmethod
    def obtener_por_id(item_id: int) -> ItemInventario:
        return ItemInventario.objects.get(id=item_id)

    @staticmethod
    def filtrar(tipo: str = None, estado: str = None) -> list:
        queryset = ItemInventario.objects.all()
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @staticmethod
    def crear(datos: dict, usuario) -> ItemInventario:
        item = ItemInventario(gestionado_por=usuario, **datos)
        item.save()
        return item

    @staticmethod
    def actualizar(item: ItemInventario, datos: dict) -> ItemInventario:
        for campo, valor in datos.items():
            setattr(item, campo, valor)
        item.save()
        return item

    @staticmethod
    def eliminar(item: ItemInventario) -> None:
        item.delete()