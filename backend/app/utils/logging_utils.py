#!/usr/bin/env python3
"""
Module pour ajouter du logging détaillé avec stack trace
"""

import logging
import traceback
import sys
from typing import Any, Optional

def log_exception_with_traceback(logger: logging.Logger, exception: Exception, context: dict = None):
    """
    Log une exception avec stack trace détaillé
    
    Args:
        logger: Logger instance
        exception: L'exception à logger
        context: Dictionnaire optionnel avec contexte supplémentaire
    """
    context = context or {}
    
    # Construire le message d'erreur détaillé
    error_message = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ EXCEPTION DÉTAILLÉE
╠════════════════════════════════════════════════════════════════════════════╣
║
║ Type: {type(exception).__name__}
║ Message: {str(exception)}
║ Module: {exception.__class__.__module__}
║
"""
    
    if context:
        error_message += "║ CONTEXTE:\n"
        for key, value in context.items():
            error_message += f"║   - {key}: {value}\n"
    
    error_message += "║\n║ STACK TRACE:\n"
    
    # Ajouter le stack trace
    tb_lines = traceback.format_exception(type(exception), exception, exception.__traceback__)
    for line in tb_lines:
        for tb_line in line.rstrip('\n').split('\n'):
            error_message += f"║   {tb_line}\n"
    
    error_message += """║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    logger.error(error_message, exc_info=True)


def log_full_traceback(logger: logging.Logger, message: str = "Full Stack Trace"):
    """
    Log le stack trace complet du point courant
    """
    tb_lines = traceback.format_stack()
    
    full_message = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ {message.upper()}
╠════════════════════════════════════════════════════════════════════════════╣
"""
    
    for line in tb_lines:
        for tb_line in line.rstrip('\n').split('\n'):
            full_message += f"║ {tb_line}\n"
    
    full_message += """╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    logger.debug(full_message)
