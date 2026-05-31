import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import confusion_matrix, accuracy_score, r2_score, mean_squared_error
from scipy import signal
from scipy.ndimage import gaussian_filter
from datetime import datetime, timedelta
import json, io, base64
from flask import Flask, render_template, jsonify, request
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║        AI-BASED CROP HEALTH & SOIL MONITORING SYSTEM                         ║
║        Using Hyperspectral Imaging & Machine Learning                        ║
║                                                                               ║
║                    🌱 AgriTech Pro 🌱                                         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA PROCESSING & MODEL CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class HyperspectralDataLoader:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def generate_synthetic_data(self, n_samples=800, n_bands=112, n_classes=5):
        X, y = [], []
        class_names = ['Healthy', 'Nutrient_Deficiency', 'Pest_Infection', 'Water_Stress', 'Disease']
        
        # Create unequal distribution for more realistic data
        class_distribution = {
            'Healthy': 0.25,                    # 25%
            'Nutrient_Deficiency': 0.219,      # 21.9%
            'Pest_Infection': 0.194,           # 19.4%
            'Water_Stress': 0.188,             # 18.8%
            'Disease': 0.150                   # 15.0%
        }
        
        for class_idx, class_name in enumerate(class_names):
            # Calculate samples for this class based on distribution
            n_class_samples = int(n_samples * class_distribution[class_name])
            wavelengths = np.linspace(400, 2500, n_bands)
            
            if class_name == 'Healthy':
                signature = self._healthy_signature(wavelengths)
            elif class_name == 'Nutrient_Deficiency':
                signature = self._nutrient_deficiency_signature(wavelengths)
            elif class_name == 'Pest_Infection':
                signature = self._pest_infection_signature(wavelengths)
            elif class_name == 'Water_Stress':
                signature = self._water_stress_signature(wavelengths)
            else:
                signature = self._disease_signature(wavelengths)

            for _ in range(n_class_samples):
                noise = np.random.normal(0, 0.05, n_bands)
                sample = signature + noise
                sample = gaussian_filter(sample, sigma=1)
                X.append(sample)
                y.append(class_idx)

        X, y = np.array(X), np.array(y)
        indices = np.random.permutation(len(X))
        return X[indices], y[indices], class_names

    def _healthy_signature(self, w):
        s = np.zeros_like(w)
        s += 0.05 * (w < 700)
        s += 0.5 * ((w >= 700) & (w < 1300))
        s += 0.3 * (w >= 1300)
        s[np.abs(w - 680) < 20] = 0.02
        return s

    def _nutrient_deficiency_signature(self, w):
        s = self._healthy_signature(w)
        s[w < 700] *= 1.3
        s[(w >= 700) & (w < 1300)] *= 0.8
        return s

    def _pest_infection_signature(self, w):
        s = self._healthy_signature(w)
        s[(w >= 700) & (w < 1300)] *= 0.7
        s[w > 1300] *= 1.2
        return s

    def _water_stress_signature(self, w):
        s = self._healthy_signature(w)
        s[(w > 1400) & (w < 1900)] *= 0.6
        s[(w > 700) & (w < 1300)] *= 0.85
        return s

    def _disease_signature(self, w):
        s = self._healthy_signature(w)
        s *= 0.75
        s[w < 550] *= 1.4
        return s

    def preprocess_data(self, X, y):
        X_normalized = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
        X_filtered = np.array([signal.savgol_filter(x, 7, 2) for x in X_normalized])
        X_scaled = self.scaler.fit_transform(X_filtered)
        y_encoded = self.label_encoder.fit_transform(y)
        return X_scaled, y_encoded


class SoilAnalyzer:
    def __init__(self):
        self.models = {'organic_matter': None, 'nitrogen': None, 'ph': None, 'moisture': None}
        self.scalers = {k: StandardScaler() for k in self.models.keys()}

    def generate_soil_data(self, n_samples=800, n_bands=112):
        X, y_organic, y_nitrogen, y_ph, y_moisture = [], [], [], [], []
        wavelengths = np.linspace(400, 2500, n_bands)

        for _ in range(n_samples):
            organic_matter = np.random.uniform(1.0, 8.0)
            nitrogen = np.random.uniform(0.05, 0.5)
            ph = np.random.uniform(5.0, 8.5)
            moisture = np.random.uniform(10, 40)

            signature = self._soil_signature(wavelengths, organic_matter, nitrogen, ph, moisture)
            X.append(signature + np.random.normal(0, 0.03, n_bands))
            y_organic.append(organic_matter)
            y_nitrogen.append(nitrogen)
            y_ph.append(ph)
            y_moisture.append(moisture)

        return np.array(X), {
            'organic_matter': np.array(y_organic),
            'nitrogen': np.array(y_nitrogen),
            'ph': np.array(y_ph),
            'moisture': np.array(y_moisture)
        }

    def _soil_signature(self, wavelengths, organic_matter, nitrogen, ph, moisture):
        signature = np.ones_like(wavelengths) * 0.2
        signature[(wavelengths > 400) & (wavelengths < 700)] *= (1 - organic_matter * 0.08)
        signature[(wavelengths > 1500) & (wavelengths < 1800)] *= (1 - nitrogen * 0.3)
        signature[(wavelengths > 2000) & (wavelengths < 2300)] *= (0.8 + ph * 0.03)
        signature[(wavelengths > 1400) & (wavelengths < 1500)] *= (1 - moisture * 0.02)
        signature[(wavelengths > 1900) & (wavelengths < 2000)] *= (1 - moisture * 0.025)
        return signature

    def train_models(self, X, y):
        results = {}
        for property_name, y_values in y.items():
            X_train, X_test, y_train, y_test = train_test_split(X, y_values, test_size=0.2, random_state=42)
            X_train_scaled = self.scalers[property_name].fit_transform(X_train)
            X_test_scaled = self.scalers[property_name].transform(X_test)

            model = GradientBoostingRegressor(n_estimators=50, max_depth=4, learning_rate=0.1, subsample=0.8, random_state=42)
            model.fit(X_train_scaled, y_train)
            self.models[property_name] = model

            y_pred = model.predict(X_test_scaled)
            results[property_name] = {'y_test': y_test, 'y_pred': y_pred}

        return results


class PesticideAnalyzer:
    def generate_field_map(self, width=50, height=50, n_bands=112):
        field_map = np.zeros((height, width, n_bands))
        pesticide_map = np.zeros((height, width))

        self._add_application_zone(field_map, pesticide_map, (12, 12), (12, 25), 1.0, 0.9)
        self._add_application_zone(field_map, pesticide_map, (30, 5), (17, 17), 1.8, 0.7)
        self._add_application_zone(field_map, pesticide_map, (15, 35), (20, 12), 0.4, 0.85)
        self._add_application_zone(field_map, pesticide_map, (37, 35), (10, 12), 0.0, 1.0)

        return field_map, pesticide_map

    def _add_application_zone(self, field_map, pesticide_map, position, size, intensity, uniformity):
        x, y = position
        w, h = size
        wavelengths = np.linspace(400, 2500, field_map.shape[2])

        for i in range(h):
            for j in range(w):
                if y+i < field_map.shape[0] and x+j < field_map.shape[1]:
                    local_intensity = intensity * (uniformity + (1-uniformity) * np.random.random())
                    signature = self._pesticide_signature(wavelengths, local_intensity)
                    field_map[y+i, x+j, :] = signature
                    pesticide_map[y+i, x+j] = local_intensity

    def _pesticide_signature(self, wavelengths, intensity):
        signature = np.zeros_like(wavelengths)
        signature += 0.05 * (wavelengths < 700)
        signature += 0.45 * ((wavelengths >= 700) & (wavelengths < 1300))
        signature += 0.25 * (wavelengths >= 1300)

        if intensity > 0:
            signature[(wavelengths > 1200) & (wavelengths < 1400)] *= (1 - intensity * 0.3)
            signature[(wavelengths > 1700) & (wavelengths < 1900)] *= (1 - intensity * 0.25)
            signature[wavelengths < 700] *= (1 + intensity * 0.4)

        signature += np.random.normal(0, 0.02, len(wavelengths))
        return np.clip(signature, 0, 1)

    def detect_application_issues(self, field_map):
        pesticide_index = self._calculate_pesticide_index(field_map)

        classification = np.zeros_like(pesticide_index, dtype=int)
        classification[pesticide_index < 0.2] = 0
        classification[(pesticide_index >= 0.2) & (pesticide_index < 0.6)] = 1
        classification[(pesticide_index >= 0.6) & (pesticide_index < 1.2)] = 2
        classification[pesticide_index >= 1.2] = 3

        total_pixels = classification.size
        stats = {
            'missed': np.sum(classification == 0) / total_pixels * 100,
            'under_applied': np.sum(classification == 1) / total_pixels * 100,
            'optimal': np.sum(classification == 2) / total_pixels * 100,
            'over_applied': np.sum(classification == 3) / total_pixels * 100
        }

        return classification, pesticide_index, stats

    def _calculate_pesticide_index(self, field_map):
        band_1300 = field_map[:, :, 50]
        band_1800 = field_map[:, :, 75]
        visible = field_map[:, :, 10]
        chemical_index = 1 - (band_1300 + band_1800) / 2
        coating_index = visible - 0.1
        pesticide_index = (chemical_index + coating_index) * 2
        return np.clip(pesticide_index, 0, 2)


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL STATE
# ═══════════════════════════════════════════════════════════════════════════════

class SystemState:
    def __init__(self):
        self.initialized = False
        self.X_crop = None
        self.y_crop = None
        self.class_names = None
        self.X_soil = None
        self.y_soil = None
        self.soil_results = None
        self.field_map = None
        self.classification = None
        self.pesticide_index = None
        self.pesticide_stats = None
        self.monitoring_data = None
        self.crop_model = None
        self.crop_predictions = None

system_state = SystemState()


def initialize_system():
    # Always regenerate fresh synthetic data for each page load
    print("Initializing crop monitoring system...")

    # Crop data - fresh random data each time
    data_loader = HyperspectralDataLoader()
    system_state.X_crop, system_state.y_crop, system_state.class_names = data_loader.generate_synthetic_data()
    system_state.X_crop, system_state.y_crop = data_loader.preprocess_data(system_state.X_crop, system_state.y_crop)

    # Train crop model
    X_train, X_test, y_train, y_test = train_test_split(system_state.X_crop, system_state.y_crop, test_size=0.2, stratify=system_state.y_crop)
    
    system_state.crop_model = RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1)
    system_state.crop_model.fit(X_train, y_train)
    system_state.crop_predictions = system_state.crop_model.predict_proba(X_test)
    
    crop_acc = accuracy_score(y_test, np.argmax(system_state.crop_predictions, axis=1))
    print(f"Crop Health Model Accuracy: {crop_acc*100:.2f}%")

    # Soil data - fresh random data each time
    soil_analyzer = SoilAnalyzer()
    system_state.X_soil, system_state.y_soil = soil_analyzer.generate_soil_data()
    system_state.soil_results = soil_analyzer.train_models(system_state.X_soil, system_state.y_soil)

    # Pesticide analysis
    pesticide_analyzer = PesticideAnalyzer()
    system_state.field_map, _ = pesticide_analyzer.generate_field_map()
    system_state.classification, system_state.pesticide_index, system_state.pesticide_stats = pesticide_analyzer.detect_application_issues(system_state.field_map)

    # Monitoring data
    generate_monitoring_data()

    print("System initialized successfully!")


def generate_monitoring_data():
    monitoring_data = {'timestamps': [], 'crop_health': [], 'soil_moisture': [], 'soil_nitrogen': [], 'pesticide_coverage': []}
    start_date = datetime.now() - timedelta(days=15)

    for day in range(15):
        current_date = start_date + timedelta(days=day)
        crop_health_score = max(50, 95 - day * 1.2 + np.random.normal(0, 3))
        soil_moisture = 25 + np.sin(day / 7 * np.pi) * 5 + np.random.normal(0, 2)
        soil_nitrogen = max(0.1, 0.25 - day * 0.003 + np.random.normal(0, 0.02))
        pesticide_coverage = min(100, 60 + day * 1.5 + np.random.normal(0, 5))

        monitoring_data['timestamps'].append(current_date.strftime('%Y-%m-%d'))
        monitoring_data['crop_health'].append(float(crop_health_score))
        monitoring_data['soil_moisture'].append(float(soil_moisture))
        monitoring_data['soil_nitrogen'].append(float(soil_nitrogen))
        monitoring_data['pesticide_coverage'].append(float(pesticide_coverage))

    system_state.monitoring_data = monitoring_data


def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url


# ═══════════════════════════════════════════════════════════════════════════════
# FLASK ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    initialize_system()  # Regenerate fresh data on each page load
    return render_template('index.html')


@app.route('/api/get-graph', methods=['POST'])
def get_graph():
    initialize_system()  # Fresh data for each graph request
    data = request.json
    graph_type = data.get('graph_type')

    try:
        if graph_type == 'spectral_signatures':
            plot_url = generate_spectral_signatures()
        elif graph_type == 'soil_properties':
            plot_url = generate_soil_properties()
        elif graph_type == 'pesticide_distribution':
            plot_url = generate_pesticide_distribution()
        elif graph_type == 'monitoring_timeline':
            plot_url = generate_monitoring_timeline()
        elif graph_type == 'crop_health_distribution':
            plot_url = generate_crop_health_distribution()
        else:
            return jsonify({'error': 'Unknown graph type'}), 400

        return jsonify({'graph': plot_url, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-stats', methods=['GET'])
def get_stats():
    initialize_system()  # Fresh data for each stats request

    # Calculate crop distribution percentages
    crop_distribution = np.bincount(system_state.y_crop)
    total_crops = len(system_state.y_crop)
    crop_percentages = {
        system_state.class_names[i]: float((crop_distribution[i] / total_crops) * 100)
        for i in range(len(system_state.class_names))
    }

    stats = {
        'crop_classes': system_state.class_names,
        'crop_distribution': [int(c) for c in crop_distribution],
        'crop_percentages': crop_percentages,
        'soil_stats': {
            'organic_matter': {
                'mean': float(np.mean(system_state.y_soil['organic_matter'])),
                'std': float(np.std(system_state.y_soil['organic_matter']))
            },
            'nitrogen': {
                'mean': float(np.mean(system_state.y_soil['nitrogen'])),
                'std': float(np.std(system_state.y_soil['nitrogen']))
            },
            'ph': {
                'mean': float(np.mean(system_state.y_soil['ph'])),
                'std': float(np.std(system_state.y_soil['ph']))
            },
            'moisture': {
                'mean': float(np.mean(system_state.y_soil['moisture'])),
                'std': float(np.std(system_state.y_soil['moisture']))
            }
        },
        'pesticide_coverage': system_state.pesticide_stats,
        'current_monitoring': {
            'crop_health': system_state.monitoring_data['crop_health'][-1],
            'soil_moisture': system_state.monitoring_data['soil_moisture'][-1],
            'soil_nitrogen': system_state.monitoring_data['soil_nitrogen'][-1],
            'pesticide_coverage': system_state.monitoring_data['pesticide_coverage'][-1]
        }
    }

    return jsonify(stats)


# ═══════════════════════════════════════════════════════════════════════════════
# GRAPH GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_spectral_signatures():
    fig, axes = plt.subplots(1, 5, figsize=(16, 4))
    wavelengths = np.linspace(400, 2500, system_state.X_crop.shape[1])

    for class_idx in range(len(system_state.class_names)):
        class_samples = system_state.X_crop[system_state.y_crop == class_idx][:3]
        for sample in class_samples:
            axes[class_idx].plot(wavelengths, sample, alpha=0.7, linewidth=1.5, color='#2E8B57')

        axes[class_idx].set_title(system_state.class_names[class_idx], fontsize=11, fontweight='bold')
        axes[class_idx].set_xlabel('Wavelength (nm)', fontsize=9)
        axes[class_idx].set_ylabel('Reflectance', fontsize=9)
        axes[class_idx].grid(True, alpha=0.3)
        axes[class_idx].set_facecolor('#f8f9fa')

    fig.patch.set_facecolor('#ffffff')
    return fig_to_base64(fig)


def generate_soil_properties():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    properties = list(system_state.soil_results.keys())
    colors = ['#2E8B57', '#1E90FF', '#FF6347', '#FFD700']

    for idx, prop in enumerate(properties):
        result = system_state.soil_results[prop]
        axes[idx].scatter(result['y_test'], result['y_pred'], alpha=0.6, color=colors[idx], s=50)
        min_val = min(result['y_test'].min(), result['y_pred'].min())
        max_val = max(result['y_test'].max(), result['y_pred'].max())
        axes[idx].plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.8, linewidth=2)
        axes[idx].set_title(f'{prop.replace("_", " ").title()}', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Actual Value', fontsize=9)
        axes[idx].set_ylabel('Predicted Value', fontsize=9)
        axes[idx].grid(True, alpha=0.3)
        axes[idx].set_facecolor('#f8f9fa')

    fig.patch.set_facecolor('#ffffff')
    return fig_to_base64(fig)


def generate_pesticide_distribution():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    im1 = axes[0].imshow(system_state.pesticide_index, cmap='RdYlGn_r', aspect='auto')
    axes[0].set_title('Pesticide Distribution Index', fontsize=11, fontweight='bold')
    plt.colorbar(im1, ax=axes[0])

    classification_colors = ['#ffffff', '#FFD700', '#2E8B57', '#FF6347']
    classification_cmap = plt.cm.colors.ListedColormap(classification_colors)
    im2 = axes[1].imshow(system_state.classification, cmap=classification_cmap, aspect='auto', vmin=0, vmax=3)
    axes[1].set_title('Application Quality Map', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(im2, ax=axes[1], ticks=[0.375, 1.125, 1.875, 2.625])
    cbar.ax.set_yticklabels(['Missed', 'Under', 'Optimal', 'Over'])

    labels = list(system_state.pesticide_stats.keys())
    sizes = list(system_state.pesticide_stats.values())
    colors = ['#FF6347', '#FFD700', '#2E8B57', '#FF4500']
    axes[2].pie(sizes, labels=[l.title() for l in labels], colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    axes[2].set_title('Coverage Analysis', fontsize=11, fontweight='bold')

    fig.patch.set_facecolor('#ffffff')
    return fig_to_base64(fig)


def generate_monitoring_timeline():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()

    metrics = [
        ('crop_health', 'Crop Health (%)', '#2E8B57'),
        ('soil_moisture', 'Soil Moisture (%)', '#1E90FF'),
        ('soil_nitrogen', 'Soil Nitrogen (%)', '#FF6347'),
        ('pesticide_coverage', 'Pesticide Coverage (%)', '#FFD700')
    ]

    for idx, (metric, title, color) in enumerate(metrics):
        axes[idx].plot(range(len(system_state.monitoring_data[metric])), system_state.monitoring_data[metric], color=color, linewidth=2.5, marker='o', markersize=6)
        axes[idx].set_title(title, fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Days', fontsize=9)
        axes[idx].set_ylabel(title, fontsize=9)
        axes[idx].grid(True, alpha=0.3)
        axes[idx].set_facecolor('#f8f9fa')

    fig.patch.set_facecolor('#ffffff')
    plt.tight_layout()
    return fig_to_base64(fig)


def generate_crop_health_distribution():
    fig, ax = plt.subplots(figsize=(10, 6))

    distribution = np.bincount(system_state.y_crop)
    colors = ['#2E8B57', '#FF6347', '#1E90FF', '#FFD700', '#8A2BE2']

    bars = ax.bar(system_state.class_names, distribution, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    ax.set_ylabel('Number of Samples', fontsize=11, fontweight='bold')
    ax.set_title('Crop Health Distribution', fontsize=13, fontweight='bold')
    ax.set_facecolor('#f8f9fa')
    ax.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom', fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    fig.patch.set_facecolor('#ffffff')
    plt.tight_layout()
    return fig_to_base64(fig)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Crop Health Monitoring System...")
    app.run(debug=True, host='0.0.0.0', port=5000)
