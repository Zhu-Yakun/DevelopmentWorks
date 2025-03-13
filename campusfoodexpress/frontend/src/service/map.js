import axios from '../utils/axios'

export function getMarkers() {
  return axios.get('/restaurant/marker',
    {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
    }
  );
}

export const searchResturants = async (restaurantName) => {
  try {
    const response = await axios.get('/restaurant/get_by_name', {
      params: { restaurantName },
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    }
  );
    return response;
  } catch (error) {
    throw new Error('搜索标记数据失败');
  }
};
