"""
OMNICore Security Layer - Advanced threat detection and protection
"""
import logging
import hashlib
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import request
import hmac
import secrets

logger = logging.getLogger(__name__)

class SecurityLayer:
    """Advanced security monitoring and protection system"""
    
    def __init__(self):
        self.security_log = "data/security_events.json"
        self.blocked_ips = set()
        self.rate_limits = {}  # IP -> {requests: count, reset_time: timestamp}
        self.security_events = []
        
        # Security configuration
        self.max_requests_per_minute = 60
        self.max_requests_per_hour = 1000
        self.suspicious_patterns = [
            "sql injection",
            "xss attack",
            "directory traversal",
            "command injection"
        ]
        
        # Initialize data storage
        self._ensure_data_directory()
        self.load_security_data()
        
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def sentinel_scan(self, request_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Comprehensive security scan and threat detection"""
        try:
            scan_result = {
                "timestamp": datetime.now().isoformat(),
                "scan_id": self._generate_scan_id(),
                "threat_level": "low",
                "threats_detected": [],
                "security_score": 100,
                "recommendations": []
            }
            
            # Get client IP if request data is provided
            client_ip = None
            if request_data or (hasattr(request, 'remote_addr') and request.remote_addr):
                client_ip = request_data.get('client_ip') if request_data else request.remote_addr
                
                # IP-based security checks
                ip_analysis = self._analyze_ip_security(client_ip)
                scan_result.update(ip_analysis)
            
            # System-wide security checks
            system_security = self._check_system_security()
            scan_result["system_security"] = system_security
            
            # Update threat level based on findings
            if scan_result["threats_detected"]:
                scan_result["threat_level"] = self._calculate_threat_level(scan_result["threats_detected"])
                scan_result["security_score"] = max(0, 100 - len(scan_result["threats_detected"]) * 15)
            
            # Generate recommendations
            scan_result["recommendations"] = self._generate_security_recommendations(scan_result)
            
            # Log security event
            self._log_security_event(scan_result)
            
            return scan_result
            
        except Exception as e:
            logger.error(f"Error in security scan: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
                "threat_level": "unknown"
            }
    
    def _generate_scan_id(self) -> str:
        """Generate unique scan identifier"""
        return hashlib.md5(f"{time.time()}_{secrets.token_hex(8)}".encode()).hexdigest()[:12]
    
    def _analyze_ip_security(self, client_ip: str) -> Dict[str, Any]:
        """Analyze IP-based security threats"""
        threats = []
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            threats.append({
                "type": "blocked_ip",
                "severity": "high",
                "description": f"Request from blocked IP: {client_ip}"
            })
        
        # Rate limiting check
        rate_limit_result = self._check_rate_limit(client_ip)
        if not rate_limit_result["allowed"]:
            threats.append({
                "type": "rate_limit_exceeded",
                "severity": "medium", 
                "description": f"Rate limit exceeded for IP: {client_ip}"
            })
        
        # Suspicious request pattern detection
        if hasattr(request, 'data') and request.data:
            pattern_result = self._detect_suspicious_patterns(request.data.decode('utf-8', errors='ignore'))
            if pattern_result["suspicious"]:
                threats.extend(pattern_result["threats"])
        
        return {
            "client_ip": client_ip,
            "rate_limit_status": rate_limit_result,
            "threats_detected": threats
        }
    
    def _check_rate_limit(self, client_ip: str) -> Dict[str, Any]:
        """Check and enforce rate limiting"""
        current_time = time.time()
        current_minute = int(current_time // 60)
        current_hour = int(current_time // 3600)
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = {
                "minute_requests": 0,
                "hour_requests": 0,
                "last_minute": current_minute,
                "last_hour": current_hour,
                "last_request": current_time
            }
        
        ip_data = self.rate_limits[client_ip]
        
        # Reset counters if time period changed
        if current_minute != ip_data["last_minute"]:
            ip_data["minute_requests"] = 0
            ip_data["last_minute"] = current_minute
        
        if current_hour != ip_data["last_hour"]:
            ip_data["hour_requests"] = 0
            ip_data["last_hour"] = current_hour
        
        # Increment counters
        ip_data["minute_requests"] += 1
        ip_data["hour_requests"] += 1
        ip_data["last_request"] = current_time
        
        # Check limits
        allowed = (ip_data["minute_requests"] <= self.max_requests_per_minute and
                  ip_data["hour_requests"] <= self.max_requests_per_hour)
        
        return {
            "allowed": allowed,
            "minute_requests": ip_data["minute_requests"],
            "hour_requests": ip_data["hour_requests"],
            "minute_limit": self.max_requests_per_minute,
            "hour_limit": self.max_requests_per_hour
        }
    
    def _detect_suspicious_patterns(self, request_data: str) -> Dict[str, Any]:
        """Detect suspicious patterns in request data"""
        threats = []
        request_lower = request_data.lower()
        
        # SQL injection patterns
        sql_patterns = ["union select", "drop table", "insert into", "delete from", 
                       "' or '1'='1", "'; drop", "admin'--"]
        for pattern in sql_patterns:
            if pattern in request_lower:
                threats.append({
                    "type": "sql_injection_attempt",
                    "severity": "high",
                    "description": f"SQL injection pattern detected: {pattern}"
                })
        
        # XSS patterns
        xss_patterns = ["<script", "javascript:", "onload=", "onerror=", "eval("]
        for pattern in xss_patterns:
            if pattern in request_lower:
                threats.append({
                    "type": "xss_attempt",
                    "severity": "medium",
                    "description": f"XSS pattern detected: {pattern}"
                })
        
        # Directory traversal
        traversal_patterns = ["../", "..\\", "etc/passwd", "windows/system32"]
        for pattern in traversal_patterns:
            if pattern in request_lower:
                threats.append({
                    "type": "directory_traversal",
                    "severity": "high",
                    "description": f"Directory traversal pattern detected: {pattern}"
                })
        
        # Command injection
        command_patterns = ["; cat", "| whoami", "&& ls", "; rm", "$(", "`"]
        for pattern in command_patterns:
            if pattern in request_lower:
                threats.append({
                    "type": "command_injection",
                    "severity": "high",
                    "description": f"Command injection pattern detected: {pattern}"
                })
        
        return {
            "suspicious": len(threats) > 0,
            "threats": threats,
            "patterns_checked": len(sql_patterns) + len(xss_patterns) + len(traversal_patterns) + len(command_patterns)
        }
    
    def _check_system_security(self) -> Dict[str, Any]:
        """Check system-wide security configuration"""
        security_checks = {
            "environment_variables": self._check_env_security(),
            "file_permissions": self._check_file_permissions(),
            "network_security": self._check_network_security(),
            "encryption_status": self._check_encryption_status()
        }
        
        overall_score = sum(check.get("score", 0) for check in security_checks.values()) / len(security_checks)
        
        return {
            "checks": security_checks,
            "overall_score": round(overall_score, 1),
            "status": "secure" if overall_score > 80 else "warning" if overall_score > 60 else "vulnerable"
        }
    
    def _check_env_security(self) -> Dict[str, Any]:
        """Check environment variable security"""
        secure_vars = 0
        total_vars = 0
        issues = []
        
        sensitive_vars = ["API_KEY", "SECRET", "TOKEN", "PASSWORD", "PRIVATE_KEY"]
        
        for var_name in os.environ:
            total_vars += 1
            if any(sensitive in var_name.upper() for sensitive in sensitive_vars):
                if os.environ[var_name] and len(os.environ[var_name]) > 10:
                    secure_vars += 1
                else:
                    issues.append(f"Potentially insecure {var_name}")
        
        score = (secure_vars / max(total_vars, 1)) * 100
        
        return {
            "score": score,
            "secure_variables": secure_vars,
            "total_variables": total_vars,
            "issues": issues
        }
    
    def _check_file_permissions(self) -> Dict[str, Any]:
        """Check critical file permissions"""
        issues = []
        score = 95  # Default high score
        
        # Check critical files exist and have appropriate permissions
        critical_files = ["config.py", "main.py", ".env"]
        
        for filename in critical_files:
            if os.path.exists(filename):
                stat_info = os.stat(filename)
                # Check if file is world-readable/writable (basic check)
                if stat_info.st_mode & 0o077:  # Check others permissions
                    issues.append(f"{filename} may have overly permissive permissions")
                    score -= 10
        
        return {
            "score": max(0, score),
            "issues": issues,
            "files_checked": len(critical_files)
        }
    
    def _check_network_security(self) -> Dict[str, Any]:
        """Check network security configuration"""
        score = 85  # Default score
        issues = []
        
        # Check if running on secure port configuration
        if os.environ.get("PORT", "5000") == "80":
            issues.append("Running on HTTP port 80 without HTTPS")
            score -= 15
        
        return {
            "score": score,
            "issues": issues,
            "https_enabled": "HTTPS" in os.environ.get("PROTOCOL", "HTTP").upper()
        }
    
    def _check_encryption_status(self) -> Dict[str, Any]:
        """Check encryption and security protocols"""
        score = 90
        issues = []
        
        # Check if secret keys are properly configured
        secret_keys = ["FLASK_SECRET_KEY", "SESSION_SECRET", "STRIPE_SECRET_KEY"]
        configured_keys = sum(1 for key in secret_keys if os.environ.get(key))
        
        if configured_keys < len(secret_keys):
            issues.append(f"Only {configured_keys}/{len(secret_keys)} secret keys configured")
            score -= 20
        
        return {
            "score": score,
            "configured_secrets": configured_keys,
            "total_secrets": len(secret_keys),
            "issues": issues
        }
    
    def _calculate_threat_level(self, threats: List[Dict[str, Any]]) -> str:
        """Calculate overall threat level"""
        high_severity = sum(1 for threat in threats if threat.get("severity") == "high")
        medium_severity = sum(1 for threat in threats if threat.get("severity") == "medium")
        
        if high_severity > 0:
            return "high"
        elif medium_severity > 2:
            return "medium"
        elif medium_severity > 0 or len(threats) > 0:
            return "low"
        else:
            return "minimal"
    
    def _generate_security_recommendations(self, scan_result: Dict[str, Any]) -> List[str]:
        """Generate security improvement recommendations"""
        recommendations = []
        
        # Threat-based recommendations
        for threat in scan_result.get("threats_detected", []):
            threat_type = threat.get("type", "")
            
            if "sql_injection" in threat_type:
                recommendations.append("Implement parameterized queries and input validation")
            elif "xss" in threat_type:
                recommendations.append("Sanitize all user inputs and implement CSP headers")
            elif "rate_limit" in threat_type:
                recommendations.append("Consider implementing progressive rate limiting")
            elif "blocked_ip" in threat_type:
                recommendations.append("Review and update IP blocking policies")
        
        # System security recommendations
        system_security = scan_result.get("system_security", {})
        if system_security.get("overall_score", 100) < 80:
            recommendations.append("Address system security configuration issues")
        
        if not recommendations:
            recommendations.append("Security posture is good - maintain current protocols")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _log_security_event(self, event: Dict[str, Any]):
        """Log security event to file"""
        try:
            self.security_events.append(event)
            
            # Keep only last 100 events
            if len(self.security_events) > 100:
                self.security_events = self.security_events[-100:]
            
            with open(self.security_log, 'w') as f:
                json.dump(self.security_events, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
    
    def load_security_data(self):
        """Load security data from file"""
        try:
            with open(self.security_log, 'r') as f:
                self.security_events = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.security_events = []
    
    def block_ip(self, ip_address: str, reason: str = "Security violation"):
        """Block an IP address"""
        self.blocked_ips.add(ip_address)
        
        # Log blocking event
        block_event = {
            "timestamp": datetime.now().isoformat(),
            "action": "ip_blocked",
            "ip_address": ip_address,
            "reason": reason
        }
        
        self._log_security_event(block_event)
        logger.warning(f"IP {ip_address} blocked: {reason}")
    
    def unblock_ip(self, ip_address: str):
        """Unblock an IP address"""
        self.blocked_ips.discard(ip_address)
        
        unblock_event = {
            "timestamp": datetime.now().isoformat(),
            "action": "ip_unblocked",
            "ip_address": ip_address
        }
        
        self._log_security_event(unblock_event)
        logger.info(f"IP {ip_address} unblocked")
    
    def get_security_summary(self) -> Dict[str, Any]:
        """Get comprehensive security summary"""
        try:
            recent_events = [
                event for event in self.security_events
                if datetime.fromisoformat(event["timestamp"]) > datetime.now() - timedelta(hours=24)
            ]
            
            threat_counts = {}
            for event in recent_events:
                for threat in event.get("threats_detected", []):
                    threat_type = threat.get("type", "unknown")
                    threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
            
            return {
                "total_events_24h": len(recent_events),
                "blocked_ips": len(self.blocked_ips),
                "threat_types_24h": threat_counts,
                "most_common_threats": sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                "last_scan": self.security_events[-1]["timestamp"] if self.security_events else None,
                "security_status": "active",
                "recommendations": self._get_global_recommendations()
            }
            
        except Exception as e:
            logger.error(f"Error generating security summary: {e}")
            return {"status": "error", "error": str(e)}
    
    def _get_global_recommendations(self) -> List[str]:
        """Get global security recommendations"""
        recommendations = []
        
        # Check recent threat patterns
        if len(self.blocked_ips) > 10:
            recommendations.append("Consider implementing automatic IP unblocking after timeout")
        
        if len(self.security_events) > 50:
            recommendations.append("High security activity detected - review threat patterns")
        
        recommendations.append("Regularly update security configurations")
        recommendations.append("Monitor security logs for emerging threats")
        
        return recommendations
    
    def verify_webhook_signature(self, payload: str, signature: str, secret: str) -> bool:
        """Verify webhook signature for secure external communications"""
        try:
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(f"sha256={expected_signature}", signature)
            
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False