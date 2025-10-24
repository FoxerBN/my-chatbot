import re


def validate_simple(message: str) -> dict:
    """
    Comprehensive validation with security checks
    Returns dict with 'valid' boolean and optional 'error' message
    """

    # 1. Basic length checks
    if not message or len(message.strip()) == 0:
        return {"valid": False, "error": "Message cannot be empty"}

    if len(message) > 5000:
        return {"valid": False, "error": "Message is too long (max 5000 characters)"}

    message_lower = message.lower()

    # 2. Prompt injection detection (advanced patterns)
    prompt_injection_patterns = [
        r"ignore\s+(previous|all|your)\s+(instructions?|prompts?|rules?)",
        r"disregard\s+(previous|all|your)\s+(instructions?|prompts?|rules?)",
        r"forget\s+(previous|all|your|everything)\s+(instructions?|prompts?|rules?)",
        r"new\s+(instructions?|prompts?|rules?)\s*:",
        r"system\s*:\s*",
        r"assistant\s*:\s*",
        r"act\s+as\s+(if|though|a|an)\s+",
        r"you\s+are\s+now\s+(a|an)\s+",
        r"pretend\s+(you\s+are|to\s+be)",
        r"roleplay\s+as",
        r"</?(system|instruction|prompt|context)>",
        r"override\s+(previous|default|system)",
        r"execute\s+(code|script|command)",
    ]

    for pattern in prompt_injection_patterns:
        if re.search(pattern, message_lower):
            return {
                "valid": False,
                "error": "Message contains potentially harmful prompt injection patterns"
            }

    # 3. SQL/Code injection detection
    code_injection_patterns = [
        r"<script[^>]*>.*?</script>",
        r"javascript\s*:",
        r"on(error|load|click|mouse\w+)\s*=",
        r"(union|select|insert|update|delete|drop)\s+(all\s+)?.*\s+(from|into|table)",
        r"(exec|execute|eval|system|shell_exec)\s*\(",
    ]

    for pattern in code_injection_patterns:
        if re.search(pattern, message_lower):
            return {
                "valid": False,
                "error": "Message contains potentially harmful code injection patterns"
            }

    # 4. PII (Personal Identifiable Information) detection
    pii_patterns = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",  # Credit card
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",  # Email (case insensitive via flags)
    ]

    # Check email pattern separately with case-insensitive flag
    if re.search(pii_patterns[2], message, re.IGNORECASE):
        return {
            "valid": False,
            "error": "Please do not share personal information like email addresses"
        }

    # Check other PII patterns
    for pattern in pii_patterns[:2]:
        if re.search(pattern, message):
            return {
                "valid": False,
                "error": "Please do not share sensitive personal information"
            }

    # 5. Excessive special characters (potential obfuscation)
    special_char_ratio = len(re.findall(r"[^a-zA-Z0-9\s.,!?'-]", message)) / max(len(message), 1)
    if special_char_ratio > 0.3:
        return {
            "valid": False,
            "error": "Message contains too many special characters"
        }

    # 6. Repeated characters (spam detection)
    if re.search(r"(.)\1{10,}", message):
        return {
            "valid": False,
            "error": "Message contains excessive character repetition"
        }

    # 7. URL validation (optional - allow URLs but detect suspicious ones)
    suspicious_url_patterns = [
        r"(bit\.ly|tinyurl|goo\.gl|t\.co)/[A-Za-z0-9]+",  # URL shorteners
        r"\.tk|\.ml|\.ga|\.cf|\.gq\b",  # Free suspicious TLDs
    ]

    for pattern in suspicious_url_patterns:
        if re.search(pattern, message_lower):
            return {
                "valid": False,
                "error": "Message contains suspicious URLs"
            }

    # 8. Toxic language detection (basic)
    toxic_words = [
        r"\b(hate|kill|attack|bomb|weapon)\s+(all|every|the)\s+\w+",
        r"\b(extremely|very)\s+(offensive|harmful)\s+word",
    ]

    for pattern in toxic_words:
        if re.search(pattern, message_lower):
            return {
                "valid": False,
                "error": "Message contains inappropriate content"
            }

    return {"valid": True}
