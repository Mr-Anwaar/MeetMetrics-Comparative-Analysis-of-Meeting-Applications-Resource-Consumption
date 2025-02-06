MeetMetrics: Comparative Analysis of Meeting Applications' Resource Consumption

MeetMetrics is a research project that compares the computational and network resource usage of various online meeting applications—including TeamViewer, Skype, VooV, and Zoom—to determine their efficiency in real-time communication and online educational environments. This project provides insights for selecting the best tool for users with limited computational power.

Table of Contents

Problem Statement

Solution

Code Overview

Research Criteria

Research Method

Monitoring Details

TeamViewer

Skype

VooV

Zoom

Performance Comparison

Conclusion

License

Contact

Problem Statement

One of the challenges in assessing meeting applications is that each application (Voov, Skype, Zoom, TeamViewer) runs multiple processes during execution. To accurately measure resource usage, it is necessary to identify and monitor each process spawned by the software. Without this process-level granularity, the cumulative resource consumption cannot be properly determined.

Solution

To address this challenge, a Python script was developed that monitors system resources on a per-process basis. Each meeting application uses a specific process name for all of its processes. By filtering processes by name, the script tracks resource metrics such as CPU usage, memory consumption, and the number of threads, and logs the data into CSV files for later analysis.

Research Criteria

The objective of this research is to assess the effectiveness of online educational tools by comparing their computational and network resource usage. The research criteria include:

Computational Resources: CPU usage, memory consumption, and the number of threads per process.

Network Usage: Although not detailed in this code snippet, network metrics can also be incorporated for a more comprehensive analysis.

Research Method

Preparation

Launch the Target Software:

Start the meeting application (e.g., TeamViewer, Skype, VooV, Zoom).

Identify the Process Name:

Open Task Manager and note the process name used by the software.

Configuration

Update the Python Script:

Set process_name='[Process Name]' in the script to target the specific software.

Data Collection

Start Monitoring:

Run the Python monitoring script and use the application normally to create typical load conditions.

The script continuously records resource usage data into CSV files.

Session Management

Conduct Sessions:

Run sessions that include both periods of inactivity and periods of high activity (e.g., enabling background blur, remote access).

Stop the Session:

Close the software and stop the script once the session is complete.

Analysis

Analyze Data:

Analyze the CSV files to determine total, average, and peak resource usage.

Generate Visuals:

Create comparison tables and graphs to visualize performance across different applications.

Monitoring Details

Monitoring of TeamViewer

Process Name: TeamViewer

Procedure:

Open Task Manager and note that all processes run under the name TeamViewer.

Update the Python script with Proc_name = 'TeamViewer'.

Run a session that includes both idle and active periods.

Collect the CSV data for analysis.

Result Sample:

Row Labels

Sum of CPU

Sum of MEMORY (MB)

Sum of NUM THREADS

Example

120.6122

82466

299606.446

Grand Total

120.6122

82466

299606.446

Monitoring of Skype

Process Name: skype

Procedure:

Note that all Skype processes run under the name skype.

Update the script with Proc_name = 'skype'.

Run the Skype session (including activation of features like background blur).

Collect and analyze the CSV data.

Result Sample:

Row Labels

Sum of CPU

Sum of NUM THREADS

Sum of MEMORY (MB)

1028

0.5418

12840

68706.271

Grand Total

105.111

70945

477740.786

Monitoring of VooV

Process Name: voov

Procedure:

Identify that all VooV processes share the name voov.

Configure the script with Proc_name = 'voov'.

Conduct the monitoring session (including feature activation such as background blur).

Stop the session and collect the CSV data.

Result Sample:

Row Labels

Sum of CPU

Sum of NUM THREADS

Sum of MEMORY (MB)

Grand Total

99.1768

50684

118616.756

Performance Comparison

Name

Sum of CPU

Sum of NUM THREADS

Sum of MEMORY (MB)

TeamViewer

120.6122

299606.446

82466

Skype

105.111

70945

477740.786

VooV

99.1768

50684

118616.756

Zoom

15.8164

53223

118559.808

Conclusion

Zoom demonstrates the lowest resource consumption, making it the best option for students or users with limited computational power.

VooV is the second most efficient option.

TeamViewer and Skype have higher resource usage, suggesting that they may be less optimal for environments where hardware resources are constrained.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For any questions or feedback, please contact:

Your Name

Email: your.email@example.com

LinkedIn: Your LinkedIn
