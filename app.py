import time
from flask import Flask, request, jsonify, current_app, g as app_ctx

from repository.product_repository import ProductRepository
import engine_service.search_engine as se


from PIL import Image
# Flask API
app = Flask(__name__, static_folder='statics')
product_repos = ProductRepository('prods.json')
search_engine = se.SearchEngine()



@app.before_request
def logging_before():
    app_ctx.start_time = time.perf_counter()


@app.after_request
def logging_after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint 
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response


@app.route('/api/v1/search', methods=['POST'])
def search():
    img_file = request.files['image_request']
    size = int(request.form.get('size', 9))
    img = Image.open(img_file)
    
    if not search_engine:
        return {'error': 'Search engine is not initialized yet. Please wait and try again.'}, 500
    
    results, _ = search_engine.search(img, size)
    product_response = []
    for i in range(len(results)):
        product_id = results[i].parent.name
        product = product_repos.get_product_by_id(product_id)
        if product:
            product_response.append({
                'id': product['id'],
                'name': product['name'],
                'image': product['images'],
            })
    
    return {'products': product_response}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

