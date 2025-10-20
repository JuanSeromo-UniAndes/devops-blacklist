#!/usr/bin/env python3
"""
Script para automatizar el testing de diferentes estrategias de despliegue en AWS Elastic Beanstalk
"""
import subprocess
import time
import json
from datetime import datetime

class DeploymentTester:
    def __init__(self, app_name, env_name):
        self.app_name = app_name
        self.env_name = env_name
        self.results = []
    
    def deploy_with_strategy(self, strategy_name, config_file):
        """Ejecuta un despliegue con una estrategia específica"""
        print(f"\n=== Iniciando despliegue con estrategia: {strategy_name} ===")
        
        # Renombrar archivo de configuración activo
        subprocess.run(['copy', config_file, '.ebextensions\\deployment.config'], shell=True)
        
        start_time = time.time()
        start_datetime = datetime.now()
        
        # Ejecutar despliegue
        result = subprocess.run(['eb', 'deploy', self.env_name], 
                              capture_output=True, text=True)
        
        end_time = time.time()
        end_datetime = datetime.now()
        deployment_duration = end_time - start_time
        
        # Obtener información del entorno
        env_info = self.get_environment_info()
        
        deployment_result = {
            'strategy': strategy_name,
            'start_time': start_datetime.isoformat(),
            'end_time': end_datetime.isoformat(),
            'duration_seconds': deployment_duration,
            'duration_formatted': f"{int(deployment_duration // 60)}m {int(deployment_duration % 60)}s",
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'environment_info': env_info
        }
        
        self.results.append(deployment_result)
        
        print(f"Despliegue completado en: {deployment_result['duration_formatted']}")
        print(f"Estado: {'EXITOSO' if deployment_result['success'] else 'FALLIDO'}")
        
        return deployment_result
    
    def get_environment_info(self):
        """Obtiene información del entorno de Elastic Beanstalk"""
        try:
            result = subprocess.run(['eb', 'status', self.env_name], 
                                  capture_output=True, text=True)
            return result.stdout
        except:
            return "No se pudo obtener información del entorno"
    
    def get_instance_count(self):
        """Obtiene el número de instancias activas"""
        try:
            result = subprocess.run(['aws', 'elasticbeanstalk', 'describe-environment-resources',
                                   '--environment-name', self.env_name], 
                                  capture_output=True, text=True)
            data = json.loads(result.stdout)
            instances = data.get('EnvironmentResources', {}).get('Instances', [])
            return len(instances)
        except:
            return "No disponible"
    
    def run_all_strategies(self):
        """Ejecuta todas las estrategias de despliegue"""
        strategies = [
            ('All At Once', '.ebextensions\\deployment-all-at-once.config'),
            ('Rolling', '.ebextensions\\deployment-rolling.config'),
            ('Rolling with Additional Batch', '.ebextensions\\deployment-rolling-batch.config'),
            ('Immutable', '.ebextensions\\deployment-immutable.config')
        ]
        
        for strategy_name, config_file in strategies:
            self.deploy_with_strategy(strategy_name, config_file)
            
            # Esperar entre despliegues
            print("Esperando 2 minutos antes del siguiente despliegue...")
            time.sleep(120)
        
        self.generate_report()
    
    def generate_report(self):
        """Genera un reporte de todos los despliegues"""
        print("\n" + "="*80)
        print("REPORTE DE ESTRATEGIAS DE DESPLIEGUE")
        print("="*80)
        
        for result in self.results:
            print(f"\nEstrategia: {result['strategy']}")
            print(f"Duración: {result['duration_formatted']}")
            print(f"Estado: {'EXITOSO' if result['success'] else 'FALLIDO'}")
            print(f"Instancias: {self.get_instance_count()}")
            print("-" * 40)
        
        # Guardar reporte en archivo
        with open('deployment_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\nReporte guardado en: deployment_report.json")

if __name__ == "__main__":
    # Configurar con tus valores
    APP_NAME = "blacklist-app"  # Cambiar por tu nombre de aplicación
    ENV_NAME = "blacklist-env"  # Cambiar por tu nombre de entorno
    
    tester = DeploymentTester(APP_NAME, ENV_NAME)
    tester.run_all_strategies()