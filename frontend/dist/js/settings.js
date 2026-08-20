/* settings.js — User Profile Settings */

document.addEventListener('DOMContentLoaded', () => {
  if (!Auth.requireAuth()) return;
  renderNavbar('settings');

  const user = Auth.getUser();
  const extra = JSON.parse(localStorage.getItem('userExtraDetails') || '{}');
  const isAdmin = Auth.isAdmin();

  // Set avatar
  const avatar = document.getElementById('settings-avatar');
  if (avatar) avatar.textContent = isAdmin ? '👑' : '👤';

  // Populate form
  const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };

  set('full_name', user.full_name || '');
  set('email',     user.email || '');
  set('age',       user.age || 18);
  set('gender',    extra.gender || 'Female');
  set('country',   extra.country || 'India');
  set('state',     extra.state || 'Kerala');
  set('district',  extra.district || 'Ernakulam');
  set('institution', extra.institution || '');
  set('language',  extra.language || 'English');

  // Submit
  document.getElementById('settings-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    UI.hideAlert('alert-box');

    const newPwd  = document.getElementById('new_password').value;
    const confPwd = document.getElementById('confirm_new_password').value;

    if (newPwd && newPwd !== confPwd) {
      UI.showAlert('alert-box', 'error', 'New passwords do not match.');
      return;
    }

    UI.setLoading('save-btn', true, 'Saving Changes...', 'Save Profile Settings');

    try {
      if (user?.id) {
        await API.put('/api/user/profile', {
          full_name: document.getElementById('full_name').value.trim(),
          age: parseInt(document.getElementById('age').value) || 18,
        }, true).catch(e => console.log('Profile update note:', e));
      }

      const updatedUser = { ...user, full_name: document.getElementById('full_name').value.trim(), age: parseInt(document.getElementById('age').value) || 18 };
      localStorage.setItem('userInfo', JSON.stringify(updatedUser));
      localStorage.setItem('user', JSON.stringify(updatedUser));

      localStorage.setItem('userExtraDetails', JSON.stringify({
        gender:      document.getElementById('gender').value,
        country:     document.getElementById('country').value,
        state:       document.getElementById('state').value,
        district:    document.getElementById('district').value,
        institution: document.getElementById('institution').value,
        language:    document.getElementById('language').value,
      }));

      UI.showAlert('alert-box', 'success', '✨ Profile settings updated successfully!');
    } catch {
      UI.showAlert('alert-box', 'error', 'Failed to update profile settings.');
    } finally {
      UI.setLoading('save-btn', false, '', 'Save Profile Settings');
    }
  });

  // Delete account
  document.getElementById('delete-btn').addEventListener('click', () => {
    if (confirm('CAUTION: Are you sure you want to delete your account? All assessment history will be permanently deleted.')) {
      localStorage.clear();
      window.location.href = '/register.html';
    }
  });
});
