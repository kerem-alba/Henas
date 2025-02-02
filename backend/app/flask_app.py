from flask import Flask, jsonify, request
from flask_cors import CORS

from services.database_service import (
    get_detailed_doctors,
    get_doctors,
    add_doctor,
    update_all_doctors,
    delete_doctor,
    get_seniority,
    get_detailed_seniority,
    add_seniority,
    update_all_seniorities,
    delete_seniority,
    get_shift_areas,
    add_shift_area,
    update_all_shift_areas,
    delete_shift_area,
)
from run_algorithm import run_algorithm
import json


app = Flask(__name__)
CORS(app)


@app.route("/get-doctors", methods=["GET"])
def get_detailed_doctors_endpoint():
    try:
        doctors = get_detailed_doctors()

        formatted_doctors = [
            {
                "name": doc[0],
                "seniority_id": doc[1],
                "max_shifts_per_month": doc[2],
                "shift_areas": doc[3],
            }
            for doc in doctors
        ]
        return app.response_class(
            response=json.dumps(formatted_doctors, ensure_ascii=False),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/run-algorithm", methods=["POST"])
def run_algorithm_endpoint():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = run_algorithm(data)

        return jsonify({"schedule": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctors", methods=["GET"])
def list_doctors_endpoint():
    try:
        doctors = get_doctors()
        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/doctors", methods=["POST"])
def add_doctor_endpoint():
    try:
        data = request.json

        if not data.get("name") or not data.get("seniority_id"):
            return jsonify({"error": "name and seniority_id are required"}), 400

        new_id = add_doctor(data)

        return jsonify({"id": new_id, "message": "Doctor added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/doctors/all", methods=["PUT"])
def update_doctors_endpoint():
    try:
        data = request.json
        update_all_doctors(data)
        return jsonify({"message": "Doctors updated successfully"}), 200
    except Exception as e:
        print("Hata Ayrıntısı:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor_endpoint(doctor_id):
    try:
        delete_doctor(doctor_id)
        return jsonify({"message": "Doctor deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/seniority", methods=["GET"])
def list_seniority():
    try:
        seniority = get_seniority()
        return jsonify(seniority), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/seniority/detailed", methods=["GET"])
def list_detailed_seniority():
    try:
        seniority = get_detailed_seniority()
        return jsonify(seniority), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/seniority", methods=["POST"])
def add_seniority_endpoint():
    try:
        data = request.json

        if (
            not data.get("seniority_name")
            or not data.get("max_shifts_per_month")
            or not data.get("shift_area_ids")
        ):
            return (
                jsonify(
                    {
                        "error": "seniority_name, max_shifts_per_month, and shift_area_ids are required"
                    }
                ),
                400,
            )

        new_id = add_seniority(data)
        return jsonify({"id": new_id, "message": "Seniority added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/seniority/all", methods=["PUT"])
def update_seniorities_endpoint():
    try:
        data = request.json
        update_all_seniorities(data)
        return jsonify({"message": "Seniorities updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/seniority/<int:seniority_id>", methods=["DELETE"])
def delete_seniority_endpoint(seniority_id):
    try:
        delete_seniority(seniority_id)
        return jsonify({"message": "Seniority deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/shift-areas", methods=["GET"])
def list_shift_areas():
    try:
        shift_areas = get_shift_areas()
        return jsonify(shift_areas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@app.route("/shift-areas", methods=["POST"])
def add_shift_area_endpoint():
    try:
        data = request.json

        if not data.get("area_name"):
            return jsonify({"error": "area_name is required"}), 400

        new_id = add_shift_area(data)
        return jsonify({"id": new_id, "message": "Shift area added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/shift-areas/all", methods=["PUT"])
def update_shift_areas_endpoint():
    try:
        data = request.json
        update_all_shift_areas(data)
        return jsonify({"message": "Shift areas updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/shift-areas/<int:shift_area_id>", methods=["DELETE"])
def delete_shift_area_endpoint(shift_area_id):
    try:
        delete_shift_area(shift_area_id)
        return jsonify({"message": "Shift area deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500