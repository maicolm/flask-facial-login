from flask import Blueprint, jsonify
import os
import shutil

reinicio_bp = Blueprint('reinicio_bp', __name__)

@reinicio_bp.route('/api/reiniciar', methods=['POST'])
def reiniciar_modelo():
    try:
        # Eliminar dataset
        if os.path.exists('dataset'):
            shutil.rmtree('dataset')
            os.makedirs('dataset')

        # Eliminar modelos
        if os.path.exists('modelos/modelo_lbph.yml'):
            os.remove('modelos/modelo_lbph.yml')
        if os.path.exists('modelos/modelo_logistico.pkl'):
            os.remove('modelos/modelo_logistico.pkl')

        return jsonify({'success': True, 'message': 'Sistema reiniciado correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
