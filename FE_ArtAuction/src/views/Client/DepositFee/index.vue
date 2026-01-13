<template>
  <div class="auction-registration">
    <div class="container">
      <div class="registration-card">
        <div class="header">
          <h1>Auction Registration</h1>
          <p class="subtitle">Register to participate in our upcoming auctions</p>
        </div>

        <form @submit.prevent="handleSubmit" class="registration-form">
          <!-- Personal Information Section -->
          <section class="form-section">
            <h2>Personal Information</h2>

            <div class="form-row">
              <div class="form-group">
                <label for="firstName">First Name <span class="required">*</span></label>
                <input
                  id="firstName"
                  v-model="formData.firstName"
                  type="text"
                  placeholder="Enter your first name"
                  :class="{ 'error': errors.firstName }"
                  @blur="validateField('firstName')"
                />
                <span v-if="errors.firstName" class="error-message">{{ errors.firstName }}</span>
              </div>

              <div class="form-group">
                <label for="lastName">Last Name <span class="required">*</span></label>
                <input
                  id="lastName"
                  v-model="formData.lastName"
                  type="text"
                  placeholder="Enter your last name"
                  :class="{ 'error': errors.lastName }"
                  @blur="validateField('lastName')"
                />
                <span v-if="errors.lastName" class="error-message">{{ errors.lastName }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="email">Email Address <span class="required">*</span></label>
                <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="your.email@example.com"
                  :class="{ 'error': errors.email }"
                  @blur="validateField('email')"
                />
                <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
              </div>

              <div class="form-group">
                <label for="phone">Phone Number <span class="required">*</span></label>
                <input
                  id="phone"
                  v-model="formData.phone"
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  :class="{ 'error': errors.phone }"
                  @blur="validateField('phone')"
                />
                <span v-if="errors.phone" class="error-message">{{ errors.phone }}</span>
              </div>
            </div>
          </section>

          <!-- Address Section -->
          <section class="form-section">
            <h2>Address</h2>

            <div class="form-group">
              <label for="address">Street Address <span class="required">*</span></label>
              <input
                id="address"
                v-model="formData.address"
                type="text"
                placeholder="123 Main Street"
                :class="{ 'error': errors.address }"
                @blur="validateField('address')"
              />
              <span v-if="errors.address" class="error-message">{{ errors.address }}</span>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="city">City <span class="required">*</span></label>
                <input
                  id="city"
                  v-model="formData.city"
                  type="text"
                  placeholder="City"
                  :class="{ 'error': errors.city }"
                  @blur="validateField('city')"
                />
                <span v-if="errors.city" class="error-message">{{ errors.city }}</span>
              </div>

              <div class="form-group">
                <label for="state">State/Province <span class="required">*</span></label>
                <input
                  id="state"
                  v-model="formData.state"
                  type="text"
                  placeholder="State"
                  :class="{ 'error': errors.state }"
                  @blur="validateField('state')"
                />
                <span v-if="errors.state" class="error-message">{{ errors.state }}</span>
              </div>

              <div class="form-group">
                <label for="zipCode">Zip Code <span class="required">*</span></label>
                <input
                  id="zipCode"
                  v-model="formData.zipCode"
                  type="text"
                  placeholder="12345"
                  :class="{ 'error': errors.zipCode }"
                  @blur="validateField('zipCode')"
                />
                <span v-if="errors.zipCode" class="error-message">{{ errors.zipCode }}</span>
              </div>
            </div>
          </section>

          <!-- Bidder Information Section -->
          <section class="form-section">
            <h2>Bidder Information</h2>

            <div class="form-group">
              <label for="bidderId">Preferred Bidder ID</label>
              <input
                id="bidderId"
                v-model="formData.bidderId"
                type="text"
                placeholder="Leave blank for auto-generated ID"
              />
              <span class="help-text">If left blank, a unique ID will be assigned</span>
            </div>

            <div class="form-group">
              <label for="category">Auction Category Interest <span class="required">*</span></label>
              <select
                id="category"
                v-model="formData.category"
                :class="{ 'error': errors.category }"
                @blur="validateField('category')"
              >
                <option value="" disabled>Select a category</option>
                <option value="art">Art & Collectibles</option>
                <option value="antiques">Antiques</option>
                <option value="jewelry">Jewelry & Watches</option>
                <option value="real-estate">Real Estate</option>
                <option value="vehicles">Vehicles</option>
                <option value="electronics">Electronics</option>
                <option value="other">Other</option>
              </select>
              <span v-if="errors.category" class="error-message">{{ errors.category }}</span>
            </div>
          </section>

          <!-- Terms and Conditions -->
          <section class="form-section">
            <div class="checkbox-group">
              <input
                id="terms"
                v-model="formData.agreeToTerms"
                type="checkbox"
                :class="{ 'error': errors.agreeToTerms }"
              />
              <label for="terms">
                I agree to the <a href="#" @click.prevent="showTerms">Terms and Conditions</a>
                and <a href="#" @click.prevent="showPrivacy">Privacy Policy</a>
                <span class="required">*</span>
              </label>
            </div>
            <span v-if="errors.agreeToTerms" class="error-message">{{ errors.agreeToTerms }}</span>

            <div class="checkbox-group">
              <input
                id="newsletter"
                v-model="formData.newsletter"
                type="checkbox"
              />
              <label for="newsletter">
                Send me updates about upcoming auctions and special events
              </label>
            </div>
          </section>

          <!-- Submit Button -->
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="isSubmitting">
              <span v-if="!isSubmitting">Register for Auction</span>
              <span v-else class="loading">
                <span class="spinner"></span>
                Processing...
              </span>
            </button>
          </div>

          <!-- Success Message -->
          <div v-if="submitSuccess" class="success-message">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <div>
              <strong>Registration Successful!</strong>
              <p>Thank you for registering. Your bidder ID is: <strong>{{ bidderId }}</strong></p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Form data
const formData = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  zipCode: '',
  bidderId: '',
  category: '',
  agreeToTerms: false,
  newsletter: false
});

// Error tracking
const errors = reactive({});

// UI state
const isSubmitting = ref(false);
const submitSuccess = ref(false);
const bidderId = ref('');

// Validation rules
const validationRules = {
  firstName: (value) => {
    if (!value) return 'First name is required';
    if (value.length < 2) return 'First name must be at least 2 characters';
    return '';
  },
  lastName: (value) => {
    if (!value) return 'Last name is required';
    if (value.length < 2) return 'Last name must be at least 2 characters';
    return '';
  },
  email: (value) => {
    if (!value) return 'Email is required';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) return 'Please enter a valid email address';
    return '';
  },
  phone: (value) => {
    if (!value) return 'Phone number is required';
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    if (!phoneRegex.test(value)) return 'Please enter a valid phone number';
    return '';
  },
  address: (value) => {
    if (!value) return 'Address is required';
    return '';
  },
  city: (value) => {
    if (!value) return 'City is required';
    return '';
  },
  state: (value) => {
    if (!value) return 'State is required';
    return '';
  },
  zipCode: (value) => {
    if (!value) return 'Zip code is required';
    const zipRegex = /^\d{5}(-\d{4})?$/;
    if (!zipRegex.test(value)) return 'Please enter a valid zip code';
    return '';
  },
  category: (value) => {
    if (!value) return 'Please select a category';
    return '';
  },
  agreeToTerms: (value) => {
    if (!value) return 'You must agree to the terms and conditions';
    return '';
  }
};

// Validate single field
const validateField = (fieldName) => {
  if (validationRules[fieldName]) {
    const error = validationRules[fieldName](formData[fieldName]);
    if (error) {
      errors[fieldName] = error;
    } else {
      delete errors[fieldName];
    }
  }
};

// Validate all fields
const validateForm = () => {
  Object.keys(validationRules).forEach(field => {
    validateField(field);
  });
  return Object.keys(errors).length === 0;
};

// Generate random bidder ID
const generateBidderId = () => {
  return 'BID' + Date.now() + Math.floor(Math.random() * 1000);
};

// Handle form submission
const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;
  submitSuccess.value = false;

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Generate bidder ID if not provided
    if (!formData.bidderId) {
      bidderId.value = generateBidderId();
    } else {
      bidderId.value = formData.bidderId;
    }

    // Show success message
    submitSuccess.value = true;

    // Reset form after 3 seconds
    setTimeout(() => {
      Object.keys(formData).forEach(key => {
        if (typeof formData[key] === 'boolean') {
          formData[key] = false;
        } else {
          formData[key] = '';
        }
      });
      submitSuccess.value = false;
    }, 5000);

  } catch (error) {
    console.error('Registration error:', error);
    alert('Registration failed. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};

// Show terms modal (placeholder)
const showTerms = () => {
  alert('Terms and Conditions would be displayed here');
};

// Show privacy policy modal (placeholder)
const showPrivacy = () => {
  alert('Privacy Policy would be displayed here');
};
</script>

<style scoped>
.auction-registration {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.registration-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 3rem;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.subtitle {
  color: #718096;
  font-size: 1.1rem;
  margin: 0;
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h2 {
  font-size: 1.5rem;
  color: #2d3748;
  margin: 0 0 1.5rem 0;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.form-group label {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.required {
  color: #e53e3e;
  margin-left: 2px;
}

.form-group input,
.form-group select {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input.error,
.form-group select.error {
  border-color: #e53e3e;
}

.form-group select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23718096' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 20px;
  padding-right: 2.5rem;
}

.error-message {
  color: #e53e3e;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.help-text {
  color: #718096;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.checkbox-group {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.checkbox-group input[type="checkbox"] {
  margin-top: 0.25rem;
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #667eea;
}

.checkbox-group label {
  flex: 1;
  color: #4a5568;
  line-height: 1.6;
  cursor: pointer;
  font-weight: normal;
}

.checkbox-group a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.checkbox-group a:hover {
  text-decoration: underline;
}

.form-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 3rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.success-message {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f0fdf4;
  border: 2px solid #86efac;
  border-radius: 8px;
  display: flex;
  gap: 1rem;
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-message svg {
  color: #22c55e;
  flex-shrink: 0;
}

.success-message strong {
  color: #166534;
  display: block;
  margin-bottom: 0.5rem;
}

.success-message p {
  color: #15803d;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .registration-card {
    padding: 2rem 1.5rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .btn-primary {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .auction-registration {
    padding: 1rem 0.5rem;
  }

  .registration-card {
    padding: 1.5rem 1rem;
  }

  .header h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>
