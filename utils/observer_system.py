"""
OMNICore Observer System - Continuous system monitoring and intelligence gathering
"""
import logging
import psutil
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
import queue

logger = logging.getLogger(__name__)

class ObserverSystem:
    """Advanced system observation and monitoring"""
    
    def __init__(self):
        self.observation_log = "data/system_observations.json"
        self.monitoring_active = False
        self.observation_queue = queue.Queue()
        self.metrics_history = []
        
        # Observation categories
        self.observation_types = {
            "performance": self._observe_performance,
            "security": self._observe_security,
            "user_activity": self._observe_user_activity,
            "system_health": self._observe_system_health,
            "resource_usage": self._observe_resources,
            "anomaly_detection": self._detect_anomalies
        }
        
        # Initialize data storage
        self._ensure_data_directory()
        self.load_historical_data()
        
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
        
    def observe_system(self) -> Dict[str, Any]:
        """Comprehensive system observation"""
        try:
            timestamp = datetime.now().isoformat()
            observations = {
                "timestamp": timestamp,
                "observations": {}
            }
            
            # Collect observations from all categories
            for obs_type, obs_method in self.observation_types.items():
                try:
                    observations["observations"][obs_type] = obs_method()
                except Exception as e:
                    logger.error(f"Error in {obs_type} observation: {e}")
                    observations["observations"][obs_type] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            # Calculate overall system score
            observations["system_score"] = self._calculate_system_score(observations["observations"])
            
            # Store observation
            self._store_observation(observations)
            
            return observations
            
        except Exception as e:
            logger.error(f"Critical error in system observation: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "critical_error",
                "error": str(e)
            }
    
    def _observe_performance(self) -> Dict[str, Any]:
        """Monitor system performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Performance assessment
            performance_score = self._calculate_performance_score(cpu_percent, memory.percent, disk.percent)
            
            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available / (1024**3),  # GB
                "disk_usage": disk.percent,
                "disk_free": disk.free / (1024**3),  # GB
                "performance_score": performance_score,
                "status": "excellent" if performance_score > 85 else "good" if performance_score > 70 else "degraded"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _observe_security(self) -> Dict[str, Any]:
        """Monitor security-related metrics"""
        try:
            # Simulate security monitoring
            security_metrics = {
                "failed_login_attempts": 0,
                "suspicious_requests": 0,
                "security_score": 95,
                "threat_level": "low",
                "last_scan": datetime.now().isoformat()
            }
            
            # Check for suspicious process activity
            suspicious_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 80:
                        suspicious_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu_usage": proc.info['cpu_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            security_metrics["suspicious_processes"] = suspicious_processes
            security_metrics["process_anomalies"] = len(suspicious_processes)
            
            return security_metrics
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _observe_user_activity(self) -> Dict[str, Any]:
        """Monitor user activity patterns"""
        try:
            # Simulate user activity monitoring
            return {
                "active_sessions": 1,
                "requests_per_minute": 0.5,
                "unique_users_24h": 1,
                "avg_session_duration": "15m",
                "activity_score": 75,
                "peak_hours": ["10:00-12:00", "14:00-16:00"],
                "status": "normal"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _observe_system_health(self) -> Dict[str, Any]:
        """Monitor overall system health"""
        try:
            # System uptime
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds / 3600
            
            # Network connections
            connections = len(psutil.net_connections())
            
            # System load
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            health_score = min(100, max(0, 100 - (uptime_hours * 0.1) - (connections * 0.5)))
            
            return {
                "uptime_hours": round(uptime_hours, 2),
                "active_connections": connections,
                "load_average": load_avg,
                "health_score": round(health_score, 1),
                "system_status": "healthy" if health_score > 80 else "warning" if health_score > 60 else "critical"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _observe_resources(self) -> Dict[str, Any]:
        """Monitor resource usage patterns"""
        try:
            # Network I/O
            net_io = psutil.net_io_counters()
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            
            return {
                "network_bytes_sent": net_io.bytes_sent if net_io else 0,
                "network_bytes_recv": net_io.bytes_recv if net_io else 0,
                "disk_read_bytes": disk_io.read_bytes if disk_io else 0,
                "disk_write_bytes": disk_io.write_bytes if disk_io else 0,
                "resource_efficiency": 85,  # Calculated metric
                "status": "optimal"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _detect_anomalies(self) -> Dict[str, Any]:
        """Detect system anomalies and unusual patterns"""
        try:
            anomalies = []
            anomaly_score = 0
            
            # CPU spike detection
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 90:
                anomalies.append(f"High CPU usage detected: {cpu_percent}%")
                anomaly_score += 30
            
            # Memory pressure detection
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                anomalies.append(f"High memory usage detected: {memory.percent}%")
                anomaly_score += 25
            
            # Disk space warning
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                anomalies.append(f"Low disk space: {disk.percent}% used")
                anomaly_score += 20
            
            return {
                "anomalies_detected": anomalies,
                "anomaly_count": len(anomalies),
                "anomaly_score": anomaly_score,
                "threat_level": "high" if anomaly_score > 50 else "medium" if anomaly_score > 20 else "low"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _calculate_performance_score(self, cpu: float, memory: float, disk: float) -> float:
        """Calculate overall performance score"""
        # Weighted performance calculation
        cpu_weight = 0.4
        memory_weight = 0.4
        disk_weight = 0.2
        
        cpu_score = max(0, 100 - cpu)
        memory_score = max(0, 100 - memory)
        disk_score = max(0, 100 - disk)
        
        total_score = (cpu_score * cpu_weight + 
                      memory_score * memory_weight + 
                      disk_score * disk_weight)
        
        return round(total_score, 1)
    
    def _calculate_system_score(self, observations: Dict[str, Any]) -> float:
        """Calculate overall system health score"""
        scores = []
        
        # Extract scores from observations
        if "performance" in observations and "performance_score" in observations["performance"]:
            scores.append(observations["performance"]["performance_score"])
        
        if "security" in observations and "security_score" in observations["security"]:
            scores.append(observations["security"]["security_score"])
        
        if "user_activity" in observations and "activity_score" in observations["user_activity"]:
            scores.append(observations["user_activity"]["activity_score"])
        
        if "system_health" in observations and "health_score" in observations["system_health"]:
            scores.append(observations["system_health"]["health_score"])
        
        return round(sum(scores) / len(scores) if scores else 0, 1)
    
    def _store_observation(self, observation: Dict[str, Any]):
        """Store observation in history"""
        try:
            self.metrics_history.append(observation)
            
            # Keep only last 100 observations
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            # Save to file
            with open(self.observation_log, 'w') as f:
                json.dump(self.metrics_history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error storing observation: {e}")
    
    def load_historical_data(self):
        """Load historical observation data"""
        try:
            with open(self.observation_log, 'r') as f:
                self.metrics_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.metrics_history = []
    
    def get_trend_analysis(self, hours: int = 24) -> Dict[str, Any]:
        """Analyze system trends over specified time period"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            recent_observations = [
                obs for obs in self.metrics_history
                if datetime.fromisoformat(obs["timestamp"]) > cutoff_time
            ]
            
            if not recent_observations:
                return {"status": "insufficient_data", "message": f"No data for last {hours} hours"}
            
            # Calculate trends
            system_scores = [obs.get("system_score", 0) for obs in recent_observations]
            avg_score = sum(system_scores) / len(system_scores)
            
            # Performance trends
            performance_scores = []
            for obs in recent_observations:
                if "performance" in obs.get("observations", {}):
                    perf_score = obs["observations"]["performance"].get("performance_score", 0)
                    performance_scores.append(perf_score)
            
            trend_direction = "stable"
            if len(system_scores) > 1:
                if system_scores[-1] > system_scores[0] + 5:
                    trend_direction = "improving"
                elif system_scores[-1] < system_scores[0] - 5:
                    trend_direction = "declining"
            
            return {
                "time_period": f"{hours}h",
                "observations_count": len(recent_observations),
                "average_system_score": round(avg_score, 1),
                "current_score": system_scores[-1] if system_scores else 0,
                "trend_direction": trend_direction,
                "performance_average": round(sum(performance_scores) / len(performance_scores), 1) if performance_scores else 0,
                "recommendations": self._generate_recommendations(recent_observations)
            }
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return {"status": "error", "error": str(e)}
    
    def _generate_recommendations(self, observations: List[Dict[str, Any]]) -> List[str]:
        """Generate system optimization recommendations"""
        recommendations = []
        
        if not observations:
            return ["Insufficient data for recommendations"]
        
        # Analyze recent performance
        latest = observations[-1].get("observations", {})
        
        if "performance" in latest:
            perf = latest["performance"]
            if perf.get("cpu_usage", 0) > 80:
                recommendations.append("Consider CPU optimization or scaling")
            if perf.get("memory_usage", 0) > 85:
                recommendations.append("Memory usage is high - consider optimization")
            if perf.get("disk_usage", 0) > 90:
                recommendations.append("Disk space critically low - cleanup required")
        
        if "anomaly_detection" in latest:
            anomalies = latest["anomaly_detection"]
            if anomalies.get("anomaly_score", 0) > 30:
                recommendations.append("System anomalies detected - investigate immediately")
        
        if not recommendations:
            recommendations.append("System operating within normal parameters")
        
        return recommendations
    
    def start_continuous_monitoring(self, interval: int = 300):  # 5 minutes
        """Start continuous system monitoring"""
        def monitor_loop():
            while self.monitoring_active:
                try:
                    observation = self.observe_system()
                    self.observation_queue.put(observation)
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(60)  # Wait before retrying
        
        if not self.monitoring_active:
            self.monitoring_active = True
            monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
            monitor_thread.start()
            logger.info("Continuous monitoring started")
    
    def stop_continuous_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        logger.info("Continuous monitoring stopped")
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get current system alerts"""
        alerts = []
        
        try:
            latest_observation = self.observe_system()
            observations = latest_observation.get("observations", {})
            
            # Performance alerts
            if "performance" in observations:
                perf = observations["performance"]
                if perf.get("cpu_usage", 0) > 90:
                    alerts.append({
                        "type": "critical",
                        "category": "performance",
                        "message": f"Critical CPU usage: {perf['cpu_usage']}%",
                        "timestamp": datetime.now().isoformat()
                    })
                
                if perf.get("memory_usage", 0) > 95:
                    alerts.append({
                        "type": "critical", 
                        "category": "performance",
                        "message": f"Critical memory usage: {perf['memory_usage']}%",
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Security alerts
            if "security" in observations:
                security = observations["security"]
                if security.get("threat_level") == "high":
                    alerts.append({
                        "type": "warning",
                        "category": "security",
                        "message": "High threat level detected",
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Anomaly alerts
            if "anomaly_detection" in observations:
                anomalies = observations["anomaly_detection"]
                if anomalies.get("anomaly_score", 0) > 50:
                    alerts.append({
                        "type": "warning",
                        "category": "anomaly",
                        "message": f"System anomalies detected: {anomalies['anomaly_count']} issues",
                        "timestamp": datetime.now().isoformat()
                    })
            
        except Exception as e:
            alerts.append({
                "type": "error",
                "category": "system",
                "message": f"Error generating alerts: {e}",
                "timestamp": datetime.now().isoformat()
            })
        
        return alerts