function confirmarEliminar(id, tipo) {
    var mensaje = "¿Estás seguro que deseas eliminar este ";
    mensaje += tipo == 'libro' ? "libro y todas sus reseñas?" : "reseña?";
    if (confirm(mensaje)) {
        if (tipo == 'libro') {
            window.location.href = "{% url 'confirmar_eliminar_libro' %}" + id;
        } else {
            window.location.href = "{% url 'confirmar_eliminar_resena' %}" + id;
        }
    }
}