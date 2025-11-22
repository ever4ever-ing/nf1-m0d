from flask_app.config.mysqlconnection import connectToMySQL
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv('MYSQL_DATABASE')

class Notificacion:
    def __init__(self, data):
        self.id_notificacion = data.get('id_notificacion')
        self.id_usuario = data['id_usuario']
        self.tipo = data['tipo']  # 'union', 'salida', 'eliminacion', etc.
        self.mensaje = data['mensaje']
        self.id_partido = data.get('id_partido')
        self.leida = data.get('leida', False)
        self.created_at = data.get('created_at')

    @classmethod
    def crear(cls, data):
        """Crea una nueva notificación"""
        query = """
            INSERT INTO notificaciones (id_usuario, tipo, mensaje, id_partido, leida)
            VALUES (%(id_usuario)s, %(tipo)s, %(mensaje)s, %(id_partido)s, %(leida)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, id_usuario, solo_no_leidas=False):
        """Obtiene todas las notificaciones de un usuario"""
        query = """
            SELECT n.*, p.fecha_inicio as partido_fecha
            FROM notificaciones n
            LEFT JOIN partidos p ON n.id_partido = p.id_partido
            WHERE n.id_usuario = %(id_usuario)s
        """
        if solo_no_leidas:
            query += " AND n.leida = FALSE"
        
        query += " ORDER BY n.created_at DESC LIMIT 50;"
        
        data = {'id_usuario': id_usuario}
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        notificaciones = []
        if results:
            for row in results:
                notificaciones.append(row)
        return notificaciones

    @classmethod
    def marcar_como_leida(cls, id_notificacion):
        """Marca una notificación como leída"""
        query = """
            UPDATE notificaciones 
            SET leida = TRUE 
            WHERE id_notificacion = %(id_notificacion)s;
        """
        data = {'id_notificacion': id_notificacion}
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def marcar_todas_leidas(cls, id_usuario):
        """Marca todas las notificaciones de un usuario como leídas"""
        query = """
            UPDATE notificaciones 
            SET leida = TRUE 
            WHERE id_usuario = %(id_usuario)s AND leida = FALSE;
        """
        data = {'id_usuario': id_usuario}
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def contar_no_leidas(cls, id_usuario):
        """Cuenta las notificaciones no leídas de un usuario"""
        query = """
            SELECT COUNT(*) as total
            FROM notificaciones
            WHERE id_usuario = %(id_usuario)s AND leida = FALSE;
        """
        data = {'id_usuario': id_usuario}
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result[0]['total'] if result else 0

    @classmethod
    def eliminar(cls, id_notificacion):
        """Elimina una notificación"""
        query = """
            DELETE FROM notificaciones 
            WHERE id_notificacion = %(id_notificacion)s;
        """
        data = {'id_notificacion': id_notificacion}
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def notificar_union_partido(cls, id_partido, id_usuario_que_se_une, nombre_usuario):
        """Crea notificación cuando alguien se une a un partido"""
        from flask_app.models.partido import Partido
        
        # Obtener el organizador del partido
        partido = Partido.obtener_por_id(id_partido)
        if not partido:
            return False
        
        # Notificar al organizador
        if partido.id_organizador != id_usuario_que_se_une:
            data = {
                'id_usuario': partido.id_organizador,
                'tipo': 'union',
                'mensaje': f'{nombre_usuario} se ha unido a tu partido',
                'id_partido': id_partido,
                'leida': False
            }
            cls.crear(data)
        
        return True

    @classmethod
    def notificar_salida_partido(cls, id_partido, id_usuario_que_sale, nombre_usuario):
        """Crea notificación cuando alguien sale de un partido"""
        from flask_app.models.partido import Partido
        
        # Obtener el organizador del partido
        partido = Partido.obtener_por_id(id_partido)
        if not partido:
            return False
        
        # Notificar al organizador
        if partido.id_organizador != id_usuario_que_sale:
            data = {
                'id_usuario': partido.id_organizador,
                'tipo': 'salida',
                'mensaje': f'{nombre_usuario} ha salido de tu partido',
                'id_partido': id_partido,
                'leida': False
            }
            cls.crear(data)
        
        return True
