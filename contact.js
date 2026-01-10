// Gestion du formulaire de contact
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Récupérer les données du formulaire
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('message').value,
                newsletter: document.getElementById('newsletter').checked
            };
            
            // Validation basique
            if (!formData.name || !formData.email || !formData.subject || !formData.message) {
                alert('Veuillez remplir tous les champs obligatoires (*)');
                return;
            }
            
            // Validation de l'email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                alert('Veuillez entrer une adresse email valide');
                return;
            }
            
            // Animation du bouton
            const submitBtn = contactForm.querySelector('.submit-btn');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Envoi en cours...';
            submitBtn.disabled = true;
            
            // Simulation d'envoi (dans un vrai projet, tu enverrais les données à un serveur)
            setTimeout(() => {
                // Message de confirmation
                alert(`Merci ${formData.name} !\n\nVotre message a bien été envoyé.\nNous vous répondrons dans les 24 heures à l'adresse : ${formData.email}\n\n🌿 L'équipe EcoWood`);
                
                // Réinitialiser le formulaire
                contactForm.reset();
                
                // Restaurer le bouton
                submitBtn.textContent = '✓ Message Envoyé';
                submitBtn.style.background = 'var(--sage)';
                
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
                
            }, 1500);
        });
    }
    
    // Animation au focus des champs
    const formInputs = document.querySelectorAll('.contact-form input, .contact-form select, .contact-form textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
});
