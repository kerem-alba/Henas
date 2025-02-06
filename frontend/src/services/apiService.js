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

export const addDoctor = async (name, seniorityId) => {
  try {
    const requestData = { name, seniority_id: seniorityId };

    const response = await fetch(`${API_BASE_URL}/doctors`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, response: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Doktor eklerken hata oluştu:", error);
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

export const deleteDoctor = async (doctorId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/doctors/${doctorId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error("Doktor silerken hata oluştu:", error);
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

export const addSeniority = async (name, maxShifts, shiftAreas = []) => {
  try {
    const requestData = {
      seniority_name: name,
      max_shifts_per_month: maxShifts,
      shift_area_ids: shiftAreas.map((area) => area.id), // Shift alanlarını ID olarak gönderiyoruz
    };

    console.log("Gönderilen veri:", requestData); // Konsolda kontrol et

    const response = await fetch(`${API_BASE_URL}/seniority`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, response: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Kıdem eklerken hata oluştu:", error);
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

export const deleteSeniority = async (seniorityId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/seniority/${seniorityId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error("Kıdem silerken hata oluştu:", error);
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

    const formattedData = Object.entries(data)
      .map(([area_name, details]) => ({
        area_name,
        id: details.id,
        min_doctors_per_area: details.min_doctors_per_area,
      }))
      .sort((a, b) => a.id - b.id);

    return formattedData;
  } catch (error) {
    console.error("Nöbet alanlarını getirirken hata oluştu:", error);
    throw error;
  }
};

export const addShiftArea = async (areaName, minDoctors) => {
  try {
    const payload = { area_name: areaName, min_doctors_per_area: Number(minDoctors) };
    console.log("Gönderilen payload:", payload); // Konsolda kontrol et

    const response = await fetch(`${API_BASE_URL}/shift-areas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Nöbet alanı eklerken hata oluştu:", error);
    throw error;
  }
};

export const updateShiftAreas = async (shiftAreas) => {
  try {
    const response = await fetch(`${API_BASE_URL}/shift-areas/all`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(shiftAreas),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Nöbet alanlarını güncellerken hata oluştu:", error);
    throw error;
  }
};

export const deleteShiftArea = async (areaId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/shift-areas/${areaId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error("Nöbet alanı silerken hata oluştu:", error);
    throw error;
  }
};

export const runAlgorithm = async (scheduleData) => {
  console.log("Algoritma çalıştırılıyor:", scheduleData); // Konsolda kontrol et
  try {
    const response = await fetch(`${API_BASE_URL}/run-algorithm`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(scheduleData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Algoritmayı çalıştırırken hata oluştu:", error);
    throw error;
  }
};
