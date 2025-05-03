import axios from 'axios';

export const apiClient = axios.create({ //example of creating a client
  baseURL: '/api/v1',
});