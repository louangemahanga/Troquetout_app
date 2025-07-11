// Modal Logic
const authModal = document.getElementById('authModal');
const loginBtn = document.getElementById('loginBtn');
const signupNavBtn = document.getElementById('signupNavBtn'); // Nouveau bouton "S'inscrire"
const modalOverlay = authModal.querySelector('.modal-overlay');
const modalCloseBtn = authModal.querySelector('.modal-close');

const tabLogin = document.getElementById('tabLogin');
const tabSignup = document.getElementById('tabSignup');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const modalTitle = document.getElementById('modalTitle');

function toggleModal() {
    authModal.classList.toggle('hidden');
    authModal.classList.toggle('visible');
    // Reset to login form when closing and reopening
    showLoginForm();
}

function showLoginForm() {
    loginForm.classList.remove('hidden');
    signupForm.classList.add('hidden');
    tabLogin.classList.add('border-indigo-600', 'text-indigo-600');
    tabLogin.classList.remove('border-transparent', 'text-gray-500');
    tabSignup.classList.remove('border-indigo-600', 'text-indigo-600');
    tabSignup.classList.add('border-transparent', 'text-gray-500');
    modalTitle.textContent = 'Connexion';
}

function showSignupForm() {
    signupForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
    tabSignup.classList.add('border-indigo-600', 'text-indigo-600');
    tabSignup.classList.remove('border-transparent', 'text-gray-500');
    tabLogin.classList.remove('border-indigo-600', 'text-indigo-600');
    tabLogin.classList.add('border-transparent', 'text-gray-500');
    modalTitle.textContent = "S'inscrire";
}

// Event Listeners
loginBtn.addEventListener('click', toggleModal);
signupNavBtn.addEventListener('click', () => { // Ajout de l'écouteur pour le nouveau bouton
    toggleModal();
    showSignupForm(); // Affiche directement le formulaire d'inscription
});
modalOverlay.addEventListener('click', toggleModal);
modalCloseBtn.addEventListener('click', toggleModal);

tabLogin.addEventListener('click', showLoginForm);
tabSignup.addEventListener('click', showSignupForm);

// Close modal when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && authModal.classList.contains('visible')) {
        toggleModal();
    }
});