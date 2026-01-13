import axios from 'axios';

const BASE_URL = 'http://localhost:8081/api/admin/statistics';

/**
 * Convert date from YYYY-MM-DD (HTML input format) to dd/MM/yyyy (backend format)
 * @param {string} dateString - Date in YYYY-MM-DD format
 * @returns {string} Date in dd/MM/yyyy format
 */
function convertDateFormat(dateString) {
  if (!dateString) return '';
  const [year, month, day] = dateString.split('-');
  return `${day}/${month}/${year}`;
}

/**
 * Get authorization headers with admin token
 * @returns {object} Headers object with Authorization
 */
function getHeaders() {
  const token = localStorage.getItem('token');
  return {
    headers: {
      Authorization: token ? `Bearer ${token}` : '',
    },
  };
}

/**
 * Generic function to call statistics API
 * @param {string} endpoint - API endpoint path
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise} API response
 */
async function fetchStatistics(endpoint, begin, end) {
  try {
    console.log('=== fetchStatistics DEBUG ===');
    console.log('Endpoint:', endpoint);
    console.log('Begin (raw):', begin);
    console.log('End (raw):', end);
    console.log('Begin (converted):', convertDateFormat(begin));
    console.log('End (converted):', convertDateFormat(end));

    const requestBody = {
      begin: convertDateFormat(begin),
      end: convertDateFormat(end),
    };
    console.log('Request body:', requestBody);
    console.log('Request URL:', `${BASE_URL}${endpoint}`);
    console.log('Headers:', getHeaders());

    const response = await axios.post(
      `${BASE_URL}${endpoint}`,
      requestBody,
      getHeaders()
    );

    console.log('Response status:', response.status);
    console.log('Response data:', response.data);
    console.log('=== END DEBUG ===');

    return response.data;
  } catch (error) {
    console.error('=== fetchStatistics ERROR ===');
    console.error(`Error fetching statistics from ${endpoint}:`, error);
    console.error('Error response:', error.response?.data);
    console.error('Error status:', error.response?.status);
    console.error('=== END ERROR ===');
    throw error;
  }
}

/**
 * Get user registration statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getUsersRegistrationStats(begin, end) {
  return fetchStatistics('/users-registration', begin, end);
}

/**
 * Get auction rooms statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getAuctionRoomsStats(begin, end) {
  return fetchStatistics('/auction-rooms', begin, end);
}

/**
 * Get artworks statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getArtworksStats(begin, end) {
  return fetchStatistics('/artworks', begin, end);
}

/**
 * Get bids statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getBidsStats(begin, end) {
  return fetchStatistics('/bids', begin, end);
}

/**
 * Get reports statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getReportsStats(begin, end) {
  return fetchStatistics('/reports', begin, end);
}

/**
 * Get revenue statistics
 * @param {string} begin - Start date in YYYY-MM-DD format
 * @param {string} end - End date in YYYY-MM-DD format
 * @returns {Promise<ChartDataResponse>}
 */
export async function getRevenueStats(begin, end) {
  return fetchStatistics('/revenue', begin, end);
}
