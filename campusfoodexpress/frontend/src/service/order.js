import axios from '../utils/axios';

export const getOrderInfo = async () => {
  try {
    const response = await axios.get(`/order/get_by_delivery_person`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    console.log('获取订单信息成功')
    return response;
  } catch (error) {
    console.error('获取订单信息失败:', error); // 打印详细错误信息，方便调试
    throw new Error('搜索数据失败');
  }
};

export const getOrderById = async (order_id) => {
  try {
    const response = await axios.get(`/order/get_order_by_id/${order_id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response;
  } catch (error) {
    console.error('获取订单信息失败:', error.response ? error.response.data : error); // 打印详细错误信息
    throw new Error('搜索数据失败');
  }
};

// 向后端发送订单接收请求
export const accept_order = async (order_id, delivery_person_id) => {
  try {
    const response = await axios.put(`/order/accept_order`, {
      order_id: order_id,           // 订单ID
      delivery_person_id: delivery_person_id  // 配送员ID
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 认证 token
      }
    });
    return response; // 返回后端的响应
  } catch (error) {
    console.error('接取订单失败:', error.response ? error.response.data : error); // 打印详细错误信息
    throw new Error('搜索数据失败');
  }
};


// 向后端发送放弃订单请求
export const cancel_order = async (order_id) => {
  try {
    const response = await axios.put(`/order/cancel_order/${order_id}`, {
      order_id: order_id,           // 订单ID
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 认证 token
      }
    });
    return response; // 返回后端的响应
  } catch (error) {
    console.error('放弃订单失败:', error.response ? error.response.data : error); // 打印详细错误信息
    throw new Error('放弃订单失败');
  }
};

// 向后端发送取消订单请求
export const delete_order = async (order_id) => {
  try {
    const response = await axios.put(`/order/delete/${order_id}`, {
      order_id: order_id,           // 订单ID
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 认证 token
      }
    });
    return response; // 返回后端的响应
  } catch (error) {
    console.error('取消订单失败:', error.response ? error.response.data : error); // 打印详细错误信息
    throw new Error('取消订单失败');
  }
};

// 向后端发送完成订单请求
export const complete_order = async (order_id) => {
  try {
    const response = await axios.put(`/order/complete_order`, {
      order_id: order_id,           // 订单ID
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}` // 认证 token
      }
    });
    return response; // 返回后端的响应
  } catch (error) {
    console.error('完成订单失败:', error.response ? error.response.data : error); // 打印详细错误信息
    throw new Error('完成订单失败');
  }
};

// 获取所有订单
export const getAllOrders = async () => {
  try {
    const response = await axios.get('/order/get_all', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  } catch (error) {
    throw new Error("Failed to fetch orders");
  }
};

// 根据用户 ID 获取订单
export function getOrdersByUser() {
  return axios.get('/order/get_by_user', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 根据配送员 ID 获取订单
export function getOrdersByDeliveryPerson() {
  return axios.get('/order/get_by_delivery_person', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 获取所有“已发起”的订单
export function getInitiatedOrders() {
  return axios.get('/order/get_initiated_orders', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 接受订单
// export function acceptOrder(orderId) {
//     console.log("Sending accept order request with:", { order_id: orderId });
//     return axios.put(
//         '/order/accept_order',
//         { order_id: orderId },
//         {
//       headers: {
//                 Authorization: `Bearer ${localStorage.getItem('token')}`,
//             },
//         }
//     );
//   }


// 创建新订单
export function addOrder(data) {
  return axios.post('/order/add', data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 更新订单信息
export function updateOrder(orderId, data) {
  return axios.put(`/order/update/${orderId}`, data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 删除订单
export function deleteOrder(orderId) {
  return axios.delete(`/order/delete/${orderId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 新增地址
export function addAddress(data) {
  return axios.post('/address/add', data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}

// 获取所有地址
export function getAddresses() {
  return axios.get('/address/get_all', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });
}