import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def visualize_data(csv_files, output_dir):
    """
    Read data from multiple CSV files, calculate average resource usage,
    and generate comparison bar charts.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dataframes = []
    app_names = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            # Sanitize column names by stripping leading/trailing spaces
            df.columns = df.columns.str.strip()
            app_name = os.path.basename(file).replace('.csv', '')

            # Convert percentage strings to numeric, handling errors
            if 'CPU %' in df.columns:
                df['CPU %'] = pd.to_numeric(df['CPU %'].astype(str).str.replace('%', ''), errors='coerce')

            if 'Memory (MB)' in df.columns:
                 df['Memory (MB)'] = pd.to_numeric(df['Memory (MB)'], errors='coerce')

            if 'Num Threads' in df.columns:
                df['Num Threads'] = pd.to_numeric(df['Num Threads'], errors='coerce')


            dataframes.append(df)
            app_names.append(app_name)
        except FileNotFoundError:
            print(f"Error: The file '{file}' was not found.")
            continue
        except Exception as e:
            print(f"An error occurred while processing '{file}': {e}")
            continue

    if not dataframes:
        print("No valid data to visualize.")
        return

    # Calculate average resource usage for each application
    avg_cpu = [df['CPU %'].mean() for df in dataframes]
    avg_mem = [df['Memory (MB)'].mean() for df in dataframes]
    avg_threads = [df['Num Threads'].mean() for df in dataframes]

    # --- Generate and Save CPU Usage Bar Chart ---
    plt.figure(figsize=(10, 6))
    plt.bar(app_names, avg_cpu, color='skyblue')
    plt.xlabel('Application')
    plt.ylabel('Average CPU Usage (%)')
    plt.title('Average CPU Usage Comparison')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    cpu_chart_path = os.path.join(output_dir, 'cpu_usage_comparison.png')
    plt.savefig(cpu_chart_path)
    plt.close()
    print(f"CPU usage comparison chart saved to '{cpu_chart_path}'")

    # --- Generate and Save Memory Usage Bar Chart ---
    plt.figure(figsize=(10, 6))
    plt.bar(app_names, avg_mem, color='lightgreen')
    plt.xlabel('Application')
    plt.ylabel('Average Memory Usage (MB)')
    plt.title('Average Memory Usage Comparison')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    mem_chart_path = os.path.join(output_dir, 'memory_usage_comparison.png')
    plt.savefig(mem_chart_path)
    plt.close()
    print(f"Memory usage comparison chart saved to '{mem_chart_path}'")

    # --- Generate and Save Number of Threads Bar Chart ---
    plt.figure(figsize=(10, 6))
    plt.bar(app_names, avg_threads, color='salmon')
    plt.xlabel('Application')
    plt.ylabel('Average Number of Threads')
    plt.title('Average Number of Threads Comparison')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    threads_chart_path = os.path.join(output_dir, 'threads_comparison.png')
    plt.savefig(threads_chart_path)
    plt.close()
    print(f"Number of threads comparison chart saved to '{threads_chart_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize and compare resource consumption data from CSV files.")
    parser.add_argument("csv_files", nargs='+', help="A list of CSV files to compare.")
    parser.add_argument("--output_dir", default="graphs", help="The directory to save the output graphs.")
    args = parser.parse_args()

    visualize_data(args.csv_files, args.output_dir)