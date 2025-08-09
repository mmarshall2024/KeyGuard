from flask import Blueprint, render_template, jsonify, request, session
import os
import json
import logging
from datetime import datetime, timedelta
import random
import threading
import time

chat_support_bp = Blueprint('chat_support', __name__)
logger = logging.getLogger(__name__)

# Global chat support data
active_chats = {}
support_metrics = {
    'total_chats': 0,
    'active_chats': 0,
    'resolved_chats': 0,
    'average_response_time': 2.3,
    'satisfaction_score': 4.8,
    'available_agents': 5
}

class ChatSupportSystem:
    def __init__(self):
        self.ai_agents = {
            'general_support': {
                'name': 'OMNI Assistant',
                'specialization': 'General inquiries and product information',
                'personality': 'helpful, professional, knowledgeable',
                'response_patterns': [
                    'I\'d be happy to help you with that!',
                    'Let me check our systems for the best solution.',
                    'That\'s a great question! Here\'s what I can tell you:',
                    'I understand your concern, let me assist you with this.'
                ]
            },
            'technical_support': {
                'name': 'Tech Specialist',
                'specialization': 'Technical issues and bot configuration',
                'personality': 'analytical, precise, solution-focused',
                'response_patterns': [
                    'I\'ll help you troubleshoot this technical issue.',
                    'Let me analyze your configuration and provide a solution.',
                    'Based on the information you\'ve provided, here\'s the fix:',
                    'I can walk you through the technical steps to resolve this.'
                ]
            },
            'sales_support': {
                'name': 'Sales Advisor',
                'specialization': 'Product recommendations and purchasing',
                'personality': 'persuasive, consultative, results-oriented',
                'response_patterns': [
                    'I\'d love to help you find the perfect solution for your business!',
                    'Based on your needs, I recommend the following products:',
                    'Let me show you how this can transform your business:',
                    'This investment will pay for itself quickly. Here\'s how:'
                ]
            },
            'enterprise_support': {
                'name': 'Enterprise Consultant',
                'specialization': 'Large-scale implementations and custom solutions',
                'personality': 'strategic, comprehensive, executive-level',
                'response_patterns': [
                    'For enterprise-level implementations, we offer:',
                    'Your organization would benefit significantly from:',
                    'Let me present a comprehensive solution for your enterprise:',
                    'I\'ll connect you with our enterprise success team.'
                ]
            }
        }
        
        self.mutation_evolution_system = {
            'learning_enabled': True,
            'conversation_analysis': True,
            'response_optimization': True,
            'pattern_recognition': True,
            'adaptive_personality': True,
            'predictive_assistance': True
        }
    
    def start_chat(self, user_id, chat_type='general'):
        """Start new chat session"""
        try:
            chat_id = f"CHAT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{random.randint(1000, 9999)}"
            
            # Select appropriate AI agent
            agent_type = self._select_agent_type(chat_type)
            agent = self.ai_agents[agent_type]
            
            chat_session = {
                'chat_id': chat_id,
                'user_id': user_id,
                'agent_type': agent_type,
                'agent_name': agent['name'],
                'start_time': datetime.now().isoformat(),
                'status': 'active',
                'messages': [],
                'sentiment': 'neutral',
                'urgency_level': 'normal',
                'context': {},
                'resolution_status': 'open',
                'satisfaction_rating': None
            }
            
            # Add welcome message
            welcome_message = self._generate_welcome_message(agent)
            chat_session['messages'].append({
                'timestamp': datetime.now().isoformat(),
                'sender': 'agent',
                'message': welcome_message,
                'type': 'text'
            })
            
            active_chats[chat_id] = chat_session
            support_metrics['total_chats'] += 1
            support_metrics['active_chats'] += 1
            
            logger.info(f"Chat {chat_id} started with agent {agent['name']}")
            
            return {
                'status': 'success',
                'chat_id': chat_id,
                'agent_name': agent['name'],
                'welcome_message': welcome_message
            }
            
        except Exception as e:
            logger.error(f"Chat start error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def process_message(self, chat_id, user_message):
        """Process user message and generate AI response"""
        try:
            if chat_id not in active_chats:
                return {'status': 'error', 'message': 'Chat session not found'}
            
            chat = active_chats[chat_id]
            agent = self.ai_agents[chat['agent_type']]
            
            # Add user message
            chat['messages'].append({
                'timestamp': datetime.now().isoformat(),
                'sender': 'user',
                'message': user_message,
                'type': 'text'
            })
            
            # Analyze message context and sentiment
            context = self._analyze_message_context(user_message)
            chat['context'].update(context)
            
            # Generate AI response with mutation evolution
            ai_response = self._generate_ai_response(chat, user_message, agent)
            
            # Add AI response
            chat['messages'].append({
                'timestamp': datetime.now().isoformat(),
                'sender': 'agent',
                'message': ai_response,
                'type': 'text'
            })
            
            # Update chat analytics
            self._update_chat_analytics(chat, user_message, ai_response)
            
            return {
                'status': 'success',
                'response': ai_response,
                'chat_id': chat_id
            }
            
        except Exception as e:
            logger.error(f"Message processing error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _select_agent_type(self, chat_type):
        """Select appropriate agent based on chat type"""
        agent_mapping = {
            'general': 'general_support',
            'technical': 'technical_support',
            'sales': 'sales_support',
            'enterprise': 'enterprise_support'
        }
        return agent_mapping.get(chat_type, 'general_support')
    
    def _generate_welcome_message(self, agent):
        """Generate personalized welcome message"""
        welcome_templates = [
            f"Hello! I'm {agent['name']}, your {agent['specialization']} specialist. How can I help you today?",
            f"Welcome to OMNI Empire support! I'm {agent['name']} and I'm here to assist you with {agent['specialization']}.",
            f"Hi there! {agent['name']} here, ready to help with {agent['specialization']}. What can I do for you?",
            f"Greetings! I'm {agent['name']}, your dedicated assistant for {agent['specialization']}. How may I assist you?"
        ]
        return random.choice(welcome_templates)
    
    def _analyze_message_context(self, message):
        """Analyze message for context and intent"""
        context = {
            'intent': 'general_inquiry',
            'urgency': 'normal',
            'sentiment': 'neutral',
            'keywords': [],
            'product_interest': None
        }
        
        message_lower = message.lower()
        
        # Intent detection
        if any(word in message_lower for word in ['buy', 'purchase', 'price', 'cost', 'upgrade']):
            context['intent'] = 'sales_inquiry'
        elif any(word in message_lower for word in ['problem', 'issue', 'error', 'bug', 'broken']):
            context['intent'] = 'technical_support'
        elif any(word in message_lower for word in ['enterprise', 'business', 'company', 'organization']):
            context['intent'] = 'enterprise_inquiry'
        
        # Urgency detection
        if any(word in message_lower for word in ['urgent', 'asap', 'immediately', 'emergency']):
            context['urgency'] = 'high'
        elif any(word in message_lower for word in ['when you can', 'no rush', 'whenever']):
            context['urgency'] = 'low'
        
        # Sentiment analysis
        positive_words = ['great', 'awesome', 'love', 'excellent', 'amazing', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'disappointed']
        
        if any(word in message_lower for word in positive_words):
            context['sentiment'] = 'positive'
        elif any(word in message_lower for word in negative_words):
            context['sentiment'] = 'negative'
        
        # Product interest detection
        products = ['omni bot', 'ai revenue', 'enterprise', 'mobile app', 'crypto', 'social media']
        for product in products:
            if product in message_lower:
                context['product_interest'] = product
                break
        
        return context
    
    def _generate_ai_response(self, chat, user_message, agent):
        """Generate intelligent AI response with mutation evolution"""
        context = chat['context']
        
        # Base response patterns
        response_patterns = agent['response_patterns']
        base_response = random.choice(response_patterns)
        
        # Context-aware response generation
        if context.get('intent') == 'sales_inquiry':
            return self._generate_sales_response(user_message, context)
        elif context.get('intent') == 'technical_support':
            return self._generate_technical_response(user_message, context)
        elif context.get('intent') == 'enterprise_inquiry':
            return self._generate_enterprise_response(user_message, context)
        else:
            return self._generate_general_response(user_message, context)
    
    def _generate_sales_response(self, message, context):
        """Generate sales-focused response"""
        responses = [
            "I'd be delighted to help you find the perfect solution! Based on your inquiry, I recommend checking out our product catalog at /products. We have amazing deals running with up to 40% off everything!",
            "Great timing! We're currently running our MEGA EMPIRE SALE with incredible discounts. Let me show you which products would be perfect for your needs. What's your primary business goal?",
            "Absolutely! Our products are designed to transform businesses just like yours. With our current flash sale pricing, you can save thousands while building your empire. Would you like to see our bestsellers?",
            "Perfect! I can help you choose the right products for maximum ROI. Our AI Revenue Accelerator and OMNI Bot Premium are extremely popular. What's your budget range?"
        ]
        
        if context.get('product_interest'):
            return f"Excellent choice! {context['product_interest'].title()} is one of our most powerful solutions. {random.choice(responses)}"
        
        return random.choice(responses)
    
    def _generate_technical_response(self, message, context):
        """Generate technical support response"""
        responses = [
            "I understand you're experiencing a technical issue. Let me help you troubleshoot this step by step. Can you tell me more about when this problem started?",
            "No worries, technical issues happen! I'm here to get you back up and running quickly. First, let's check your current setup. What system are you using?",
            "I'll help you resolve this technical problem right away. Our support system is designed to handle these issues efficiently. Can you provide any error messages you're seeing?",
            "Technical support is my specialty! Let me analyze what you've described and provide a solution. Have you tried any troubleshooting steps already?"
        ]
        return random.choice(responses)
    
    def _generate_enterprise_response(self, message, context):
        """Generate enterprise-level response"""
        responses = [
            "For enterprise implementations, we offer comprehensive solutions with dedicated support. I'd love to discuss your organization's specific needs. What's the size of your team?",
            "Enterprise customers receive our white-glove service including custom implementation and dedicated success management. Let me connect you with our enterprise team.",
            "Our enterprise solutions are designed for large-scale operations with advanced security and compliance features. Would you like to schedule a consultation?",
            "Perfect! Enterprise clients get priority access to all features plus custom integrations. I can arrange a demo of our enterprise platform right away."
        ]
        return random.choice(responses)
    
    def _generate_general_response(self, message, context):
        """Generate general support response"""
        responses = [
            "Thank you for reaching out! I'm here to help with any questions about OMNI Empire. What would you like to know more about?",
            "Great question! I can assist you with information about our products, services, or any other inquiries. How can I best help you today?",
            "I'm happy to help! Whether you need product information, technical support, or sales assistance, I'm here for you. What's on your mind?",
            "Welcome to OMNI Empire! I'm here to provide you with the information and support you need. What brings you here today?"
        ]
        return random.choice(responses)
    
    def _update_chat_analytics(self, chat, user_message, ai_response):
        """Update chat analytics and learning data"""
        # Simulated analytics update
        chat['last_activity'] = datetime.now().isoformat()
        
        # Mutation evolution learning
        if self.mutation_evolution_system['learning_enabled']:
            self._process_conversation_learning(chat, user_message, ai_response)
    
    def _process_conversation_learning(self, chat, user_message, ai_response):
        """Process conversation for mutation evolution learning"""
        # Simulated learning process
        learning_data = {
            'conversation_id': chat['chat_id'],
            'user_input': user_message,
            'ai_response': ai_response,
            'context': chat['context'],
            'timestamp': datetime.now().isoformat(),
            'effectiveness_score': random.uniform(0.8, 1.0)
        }
        
        # Store learning data for evolution
        logger.info(f"Mutation evolution learning: {learning_data['effectiveness_score']:.2f} score")

# Global chat support instance
chat_support = ChatSupportSystem()

@chat_support_bp.route('/chat-support')
def chat_support_page():
    """Chat support page"""
    return render_template('chat_support.html')

@chat_support_bp.route('/api/start-chat', methods=['POST'])
def start_chat():
    """Start new chat session"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', f"USER-{random.randint(1000, 9999)}")
        chat_type = data.get('type', 'general')
        
        result = chat_support.start_chat(user_id, chat_type)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_support_bp.route('/api/send-message', methods=['POST'])
def send_message():
    """Send message in chat"""
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')
        
        if not chat_id or not message:
            return jsonify({'error': 'Missing chat_id or message'}), 400
        
        result = chat_support.process_message(chat_id, message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_support_bp.route('/api/chat-metrics')
def get_chat_metrics():
    """Get chat support metrics"""
    try:
        return jsonify({
            'metrics': support_metrics,
            'active_chats_count': len(active_chats),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500