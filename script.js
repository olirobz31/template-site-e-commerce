// Données des produits
const products = [
    {
        id: 1,
        name: "Planche à Découper Bambou",
        description: "Planche artisanale avec poignée ergonomique, idéale pour votre cuisine quotidienne.",
        price: 34.90,
        image: "product-1"
    },
    {
        id: 2,
        name: "Support Ordinateur Portable",
        description: "Design ergonomique ajustable pour un confort optimal au travail.",
        price: 49.90,
        image: "product-2"
    },
    {
        id: 3,
        name: "Set de 3 Bols en Bois",
        description: "Collection artisanale de bols sculptés à la main, parfaits pour servir.",
        price: 59.90,
        image: "product-3"
    },
    {
        id: 4,
        name: "Organisateur de Bureau",
        description: "Design minimaliste avec compartiments pour stylos, téléphone et accessoires.",
        price: 42.90,
        image: "product-4"
    },
    {
        id: 5,
        name: "Support Téléphone Écologique",
        description: "Socle élégant et stable pour smartphone, angle de vue parfait.",
        price: 24.90,
        image: "product-5"
    },
    {
        id: 6,
        name: "Plateau de Service Artisanal",
        description: "Grand plateau rectangulaire avec poignées, finition huilée premium.",
        price: 67.90,
        image: "product-6"
    },
    {
        id: 7,
        name: "Set d'Ustensiles en Bois",
        description: "Collection complète : cuillères, spatules et fourchettes durables.",
        price: 38.90,
        image: "product-7"
    },
    {
        id: 8,
        name: "Support Pot de Plante Moderne",
        description: "Présentoir élégant sur pieds, design contemporain scandinave.",
        price: 44.90,
        image: "product-8"
    },
    {
        id: 9,
        name: "Set de 4 Sous-verres",
        description: "Dessous de verre gravés à la main, motifs géométriques uniques.",
        price: 28.90,
        image: "product-9"
    },
    {
        id: 10,
        name: "Étagère Murale avec Crochets",
        description: "Rangement mural polyvalent, finition naturelle cirée.",
        price: 54.90,
        image: "product-10"
    }
];

// État du panier
let cart = [];

// Charger le panier depuis localStorage/sessionStorage au démarrage
function loadCart() {
    try {
        // Essayer localStorage d'abord
        let saved = localStorage.getItem('ecowood_cart');
        if (!saved) {
            // Fallback sur sessionStorage
            saved = sessionStorage.getItem('ecowood_cart');
        }
        cart = saved ? JSON.parse(saved) : [];
        console.log('Panier chargé:', cart);
        updateCartCount();
    } catch (e) {
        console.error('Erreur chargement panier:', e);
        cart = [];
    }
}

// Sauvegarder le panier dans localStorage ET sessionStorage
function saveCart() {
    try {
        const cartJSON = JSON.stringify(cart);
        // Sauvegarder dans les deux pour la compatibilité
        try {
            localStorage.setItem('ecowood_cart', cartJSON);
        } catch (e) {
            console.warn('localStorage non disponible:', e);
        }
        try {
            sessionStorage.setItem('ecowood_cart', cartJSON);
        } catch (e) {
            console.warn('sessionStorage non disponible:', e);
        }
        console.log('Panier sauvegardé:', cart);
    } catch (e) {
        console.error('Erreur sauvegarde panier:', e);
    }
}

// Afficher les produits
function displayProducts() {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                <span class="eco-badge">Éco-responsable</span>
                <picture>
                    <source type="image/webp" srcset="images/${product.image}-320.webp 320w, images/${product.image}-640.webp 640w, images/${product.image}-1200.webp 1200w">
                    <img src="images/${product.image}-640.jpg" srcset="images/${product.image}-320.jpg 320w, images/${product.image}-640.jpg 640w, images/${product.image}-1200.jpg 1200w" sizes="(max-width: 768px) 100vw, 640px" alt="${product.name}" loading="lazy">
                </picture>
            </div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <div class="product-price">${product.price.toFixed(2)}€</div>
                    <button class="add-to-cart" onclick="addToCart(${product.id})">
                        Ajouter
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Ajouter au panier
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    cart.push(product);
    saveCart();
    updateCartCount();
    
    // Animation de confirmation
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '✓ Ajouté';
    btn.style.background = 'var(--sage)';
    
    setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
    }, 1000);
}

// Mettre à jour le compteur du panier
function updateCartCount() {
    document.getElementById('cartCount').textContent = cart.length;
}

// Afficher/masquer le panier
function toggleCart() {
    const modal = document.getElementById('cartModal');
    modal.classList.toggle('active');
    if (modal.classList.contains('active')) {
        displayCart();
    }
}

// Afficher le contenu du panier
function displayCart() {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    const totalPrice = document.getElementById('totalPrice');

    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="empty-cart"><p>Votre panier est vide</p></div>';
        cartTotal.style.display = 'none';
        return;
    }

    const total = cart.reduce((sum, item) => sum + item.price, 0);
    
    cartItems.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price.toFixed(2)}€</div>
            </div>
            <button class="remove-item" onclick="removeFromCart(${index})">Retirer</button>
        </div>
    `).join('');

    totalPrice.textContent = total.toFixed(2);
    cartTotal.style.display = 'block';
}

// Retirer du panier
function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartCount();
    displayCart();
}

// Commander - Rediriger vers la page de paiement
function checkout() {
    if (cart.length === 0) return;
    
    // Sauvegarder le panier et rediriger
    saveCart();
    window.location.href = 'checkout.html';
}

// Initialiser l'affichage au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    loadCart();
    displayProducts();
    
    // Fermer le modal en cliquant à l'extérieur
    document.getElementById('cartModal').addEventListener('click', function(e) {
        if (e.target === this) {
            toggleCart();
        }
    });
});
