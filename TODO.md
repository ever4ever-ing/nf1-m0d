# TODO - NosFalta1

## 🔒 Mejoras de Seguridad

- [ ] **Validación de capacidad máxima**: Verificar que no se excedan los `max_jugadores` al unirse a un partido
- [ ] **Autorización mejorada**: Validar que solo el organizador pueda editar/eliminar su partido
- [ ] **CSRF Protection**: Agregar `Flask-WTF` para protección CSRF en todos los formularios
- [ ] **Sanitización de entradas**: Validar y sanitizar todos los datos de formularios antes de procesarlos
- [ ] **Sesiones seguras**: Configurar cookies seguras y tiempo de expiración de sesión

## ⚡ Mejoras de Funcionalidad

- [x] **Sistema de notificaciones**: Notificar cuando alguien se une/sale de tu partido
- [ ] **Estados de partido**: Implementar estados como "Abierto", "Lleno", "Cancelado", "Finalizado"
- [ ] **Buscador avanzado**: Filtrar por fecha, rango de fechas, número de jugadores disponibles
- [ ] **Chat o comentarios**: Sistema de comunicación entre participantes del partido
- [ ] **Sistema de calificaciones**: Valorar jugadores después de cada partido
- [ ] **Historial de partidos**: Ver partidos pasados y estadísticas personales
- [ ] **Perfil de usuario**: Página de perfil con estadísticas, historial y configuración

## 🎨 Mejoras de UX/UI

- [ ] **Confirmación de eliminación**: Modal de confirmación antes de eliminar participantes/partidos
- [ ] **Indicador de cupos visual**: Mostrar barra de progreso de cupos disponibles/ocupados
- [ ] **Responsive mejorado**: Optimizar experiencia móvil y tablet
- [ ] **Ordenamiento de partidos**: Permitir ordenar por fecha, localidad, cupos disponibles
- [ ] **Mensajes más descriptivos**: Agregar más contexto y ayuda en los flash messages
- [ ] **Loading indicators**: Mostrar spinners durante operaciones asíncronas
- [ ] **Toast notifications**: Implementar notificaciones no intrusivas

## 🔧 Mejoras Técnicas

- [ ] **Manejo de errores robusto**: Agregar try-catch en todos los controladores
- [ ] **Logging mejorado**: Implementar sistema de logs más detallado para debugging
- [ ] **Validaciones en modelo**: Mover más lógica de validación a la capa de modelo
- [ ] **Optimización de consultas**: Reducir consultas N+1 usando JOINs eficientes
- [ ] **Paginación**: Implementar paginación para listas grandes de partidos
- [ ] **Sistema de caché**: Considerar Redis para consultas frecuentes
- [ ] **Tests unitarios**: Agregar suite de pruebas con pytest
- [ ] **Tests de integración**: Probar flujos completos de usuario
- [ ] **Migraciones de BD**: Implementar sistema de migraciones (Alembic)
- [ ] **API REST**: Crear endpoints API para futuras integraciones
- [ ] **Documentación de código**: Agregar docstrings a todas las funciones

## 🚀 Funcionalidades Nuevas

- [ ] **Recordatorios automáticos**: Enviar email/SMS recordando partidos próximos
- [ ] **Integración con calendarios**: Exportar eventos a Google Calendar, iCal
- [ ] **Mapa de recintos**: Mostrar ubicación de canchas en mapa interactivo (Google Maps)
- [ ] **Lista de espera**: Si el partido está lleno, permitir unirse a lista de espera
- [ ] **Sistema de invitaciones**: Invitar amigos por email o link compartible
- [ ] **División automática en equipos**: Algoritmo para dividir jugadores equilibradamente
- [ ] **Sistema de pagos**: Integrar Stripe/PayPal si hay costos de cancha
- [ ] **Galería de fotos**: Subir y compartir fotos de los partidos
- [ ] **Estadísticas grupales**: Dashboard con métricas de la comunidad
- [ ] **Sistema de ligas**: Crear ligas/torneos con clasificación
- [ ] **Clima en tiempo real**: Mostrar pronóstico del clima para fecha del partido
- [ ] **Check-in**: Sistema de confirmación de asistencia

## 🐛 Bugs Conocidos

- [ ] Revisar validación de fechas pasadas en creación de partidos
- [ ] Verificar comportamiento al eliminar organizador de un partido
- [ ] Testear eliminación en cascada cuando se elimina un usuario

## 📝 Documentación

- [ ] README completo con instrucciones de instalación
- [ ] Guía de contribución
- [ ] Documentación de API
- [ ] Manual de usuario
- [ ] Diagrama de base de datos actualizado

## 🎯 Prioridad Alta

1. Validación de capacidad máxima
2. Confirmación de eliminación
3. Estados de partido
4. Manejo de errores robusto
5. Tests básicos

---

**Última actualización**: 21 de noviembre de 2025
