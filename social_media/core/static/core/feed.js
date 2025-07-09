function togglePostMenu(postId) {
  const menu = document.getElementById(`menu-${postId}`);
  // Close all other open menus
  document.querySelectorAll('.delete-menu').forEach(el => {
    if (el !== menu) el.style.display = 'none';
  });
  // Toggle the current one
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

function toggleProfileMenu() {
  const menu = document.getElementById('profile-menu');
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

// Close dropdown if clicked outside (for post menus and profile menu)
window.addEventListener('click', function (e) {
  // Close post delete menus if clicked outside
  document.querySelectorAll('.post-actions').forEach(action => {
    if (!action.contains(e.target)) {
      const dropdown = action.querySelector('.delete-menu');
      if (dropdown) dropdown.style.display = 'none';
    }
  });

  // Close profile menu if clicked outside
  const profileMenu = document.getElementById('profile-menu');
  const profileBtn = document.querySelector('.profile-btn');
  if (profileMenu && !profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
    profileMenu.style.display = 'none';
  }
});
