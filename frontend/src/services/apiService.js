const API_BASE_URL = "http://127.0.0.1:5000";

export const getDoctors = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/doctors`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Doktorları getirirken hata oluştu:", error);
    throw error;
  }
};

export const getSeniorities = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/seniority`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Kıdemleri getirirken hata oluştu:", error);
    throw error;
  }
};

export const getDetailedSeniorities = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/seniority/detailed`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Seniority detaylarını alırken hata oluştu:", error);
    throw error;
  }
};

export const updateDoctors = async (doctors) => {
  try {
    const response = await fetch(`${API_BASE_URL}/doctors/all`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(doctors), // Gönderilecek JSON verisi
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json(); // Backend'den gelen yanıt
  } catch (error) {
    console.error("Doktorları güncellerken hata oluştu:", error);
    throw error;
  }
};

export const getShiftAreas = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/shift-areas`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    const formattedData = Object.entries(data).map(([area_name, id]) => ({
      area_name,
      id,
    }));

    return formattedData;
  } catch (error) {
    console.error("Nöbet alanlarını getirirken hata oluştu:", error);
    throw error;
  }
};

export const updatedSeniorities = async (seniorities) => {
  try {
    const response = await fetch(`${API_BASE_URL}/seniority/all`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(seniorities),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Kıdemleri güncellerken hata oluştu:", error);
    throw error;
  }
};
