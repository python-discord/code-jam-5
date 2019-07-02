from thoughtful_termites.calculator.footprint import total_footprint

if __name__ == "__main__":
    print(f"Sample carbon usage: {total_footprint(actions={'driving': 5, 'laptop': 5})}kg CO2")
