import streamlit as st
import openai

# Set up the page
st.set_page_config(page_title="Task Breakdown Assistant", layout="centered")
st.title("🧠 Micro-Task Breakdown Assistant")
st.write("Got a task? Enter anything from 'take a shower' to 'organize a local sapphic quilting bee.' This tool will instantly generate a free downloadable, executive-dysfunction-friendly list of micro-steps.")

# Securely grab the OpenAI API key
openai.api_key = st.secrets["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"]

# The input box for the user
task_input = st.text_area("What do you need to get done?", placeholder="Type your task here...")

if st.button("Break it down for me"):
    if task_input:
        with st.spinner("Breaking it down into micro-steps..."):
            # The instructions for the AI
            system_prompt = f"""You are an executive functioning assistant for neurodivergent individuals. 
            The user wants to break down this overarching task: "{task_input}"
            Your job is to break it down into incredibly small, manageable micro-tasks.
            
            OUTPUT FORMAT: You must output ONLY valid CSV text. Do not include markdown formatting.
            The headers must be EXACTLY: Parent Task, Task Name, Description, Estimated Time, Energy Level.
            
            CRUCIAL: The 'Parent Task' for every single row MUST be exactly "{task_input}". 
            Make sure to wrap every value in double quotes so commas inside descriptions don't break the CSV format.
            
            Example:
            "{task_input}","Create new blog doc","Open Google Docs and title it appropriately","2 mins","Low"
            """

            # Call OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate the CSV."}
                ],
                temperature=0.7
            )
            
            csv_data = response.choices[0].message.content.strip()
            
            # Clean up markdown if the AI accidentally adds it
            if csv_data.startswith("```csv"):
                csv_data = csv_data[6:]
            if csv_data.endswith("```"):
                csv_data = csv_data[:-3]
            csv_data = csv_data.strip()

            st.success("Task broken down successfully!")
            
            # Show the text box to copy/paste
            st.text_area("Copy/Paste your tasks:", value=csv_data, height=300)
            
            # The magical Download CSV button
            st.download_button(
                label="📥 Download as CSV (Import to Notion/Trello)",
                data=csv_data,
                file_name="micro_tasks.csv",
                mime="text/csv"
            )
    else:
        st.warning("Please enter a task first!")
