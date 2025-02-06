import React, { useEffect, useState, useRef } from "react";
import DraggableList from "react-draggable-list";

export default function DraggableShiftAreaList({ allShiftAreas, activeAreaNames, onUpdate }) {
  const [items, setItems] = useState([]);
  const containerRef = useRef(null);

  useEffect(() => {
    // 1) shift_area_names dizisine göre, aktif olanları doğru sırada ekle
    const mappedActive = activeAreaNames
      .map((areaName) => {
        const found = allShiftAreas.find((a) => a.area_name === areaName);
        if (!found) return null; // DB'de bulunmayan isim varsa

        return {
          id: found.id,
          name: found.area_name,
          active: true,
        };
      })
      .filter(Boolean);

    // 2) allShiftAreas dizisinde olup, aktifAreaNames içinde olmayanları "pasif" olarak ekle
    const mappedPassive = allShiftAreas
      .filter((a) => !activeAreaNames.includes(a.area_name))
      .map((a) => ({
        id: a.id,
        name: a.area_name,
        active: false,
      }));

    // 3) Final liste: Aktifler DB sırasına göre + Pasifler sonda
    const finalList = [...mappedActive, ...mappedPassive];
    console.log("useEffect -> finalList:", finalList);

    setItems(finalList);
  }, [allShiftAreas, activeAreaNames]);

  // Sürükleme bitince
  const handleMoveEnd = (newList) => {
    console.log("handleMoveEnd sonrası yeni sıralama:", newList);
    setItems(newList);
    const onlyActive = newList.filter((it) => it.active).map((it) => it.name);
    onUpdate?.(onlyActive);
  };

  // Tıklayınca aktif/pasif
  const toggleActive = (id) => {
    setItems((prev) => {
      const updated = prev.map((x) => (x.id === id ? { ...x, active: !x.active } : x));
      const onlyActive = updated.filter((it) => it.active).map((it) => it.name);
      onUpdate?.(onlyActive);
      return updated;
    });
  };

  // render şablonu
  const ItemTemplate = ({ item, dragHandleProps }) => {
    const handleProps = item.active ? dragHandleProps : {};
    return (
      <div
        style={{
          padding: "4px",
          border: "1px solid #ccc",
          borderRadius: 4,
          background: item.active ? "#fff" : "#eee",
          color: item.active ? "#000" : "#999",
          cursor: item.active ? "move" : "pointer",
          display: "flex",
          justifyContent: "space-between",
        }}
        onClick={() => toggleActive(item.id)}
        {...handleProps}
      >
        {item.name}
      </div>
    );
  };

  return (
    <div ref={containerRef} style={{ touchAction: "pan-y" }}>
      <DraggableList itemKey="id" template={ItemTemplate} list={items} onMoveEnd={handleMoveEnd} container={() => containerRef.current} />
    </div>
  );
}
