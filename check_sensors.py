import json
from pathlib import Path
import pandas as pd
import yaml


def check_sensors():
	data_dir = Path(__file__).resolve().parent

	with (data_dir / "config.yml").open(encoding="utf-8") as config_file:
		config = yaml.safe_load(config_file)

	sensors = pd.read_excel(data_dir / "sensors.xlsx")
	calibrations = pd.read_csv(data_dir / "calibrations.csv")
	sensor_status = sensors.merge(
		calibrations,
		on="sensor_id",
		how="left",
		validate="one_to_one",
	)
	overdue_sensors = sensor_status.loc[
		sensor_status["days_since_calibration"] > config["max_days_since_calibration"],
		["sensor_id", "lab_room", "owner", "days_since_calibration"],
	]

	output_path = data_dir / config["output_file"]
	with output_path.open("w", encoding="utf-8") as output_file:
		json.dump(overdue_sensors.to_dict(orient="records"), output_file, indent=2)


if __name__ == "__main__":
	check_sensors()