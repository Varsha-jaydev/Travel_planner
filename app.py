import streamlit as st

from agent import build_travel_crew


st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
)


# ---------- Styling ----------

st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }

        .hero {
            padding: 2rem 0 1rem 0;
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 0.25rem;
        }

        .hero p {
            color: #64748b;
            font-size: 1.15rem;
        }

        .result {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Header ----------

st.markdown(
    """
    <div class="hero">
        <h1>✈️ AI Travel Planner</h1>
        <p>
            Build a personalized itinerary using a team of AI travel agents.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------- Sidebar / Form ----------

with st.sidebar:
    st.header("🌍 Trip Details")

    destination = st.text_input(
        "Destination",
        value="Tokyo, Japan",
        placeholder="e.g. Paris, France",
    )

    days = st.slider(
        "Number of days",
        min_value=1,
        max_value=30,
        value=7,
    )

    budget = st.number_input(
        "Total budget (USD)",
        min_value=100.0,
        max_value=100000.0,
        value=3000.0,
        step=100.0,
    )

    st.subheader("❤️ Interests")

    interests_options = [
        "Food",
        "Culture",
        "History",
        "Nature",
        "Shopping",
        "Nightlife",
        "Art",
        "Adventure",
        "Beaches",
        "Photography",
    ]

    selected_interests = st.multiselect(
        "What are you interested in?",
        interests_options,
        default=["Food", "Culture", "History"],
    )

    custom_interests = st.text_input(
        "Other interests",
        placeholder="e.g. anime, hiking, architecture",
    )

    if custom_interests:
        selected_interests.append(custom_interests)

    interests = ", ".join(selected_interests)

    st.divider()

    generate = st.button(
        "🗺️ Generate Itinerary",
        type="primary",
        use_container_width=True,
    )


# ---------- Main Content ----------

if not generate:
    st.info(
        "👈 Enter your trip details in the sidebar and click "
        "**Generate Itinerary**."
    )

    st.markdown("### How it works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            ### 🔎 Researcher
            Researches the destination, attractions, neighborhoods,
            food, transportation, and local customs.
            """
        )

    with col2:
        st.markdown(
            """
            ### 🗓️ Planner
            Turns the research into a practical day-by-day itinerary
            based on your interests.
            """
        )

    with col3:
        st.markdown(
            """
            ### 💰 Budget Analyst
            Estimates accommodation, food, transportation,
            activities, and other trip expenses.
            """
        )

else:
    if not destination.strip():
        st.error("Please enter a destination.")
        st.stop()

    if not selected_interests:
        st.warning("Please select at least one interest.")
        st.stop()

    st.markdown(
        f"""
        ## 🗺️ Your {days}-Day Trip to {destination}

        **Budget:** ${budget:,.0f}  
        **Interests:** {interests}
        """
    )

    with st.spinner(
        "🤖 Our AI travel agents are planning your trip..."
    ):
        try:
            itinerary = build_travel_crew(
                destination=destination,
                days=days,
                budget=budget,
                interests=interests,
            )

            st.success("Your itinerary is ready!")

            st.markdown(
                '<div class="result">',
                unsafe_allow_html=True,
            )

            st.markdown(itinerary)

            st.markdown("</div>", unsafe_allow_html=True)

            # Download button
            st.download_button(
                label="⬇️ Download Itinerary",
                data=itinerary,
                file_name=f"{destination.replace(',', '').replace(' ', '_')}_itinerary.txt",
                mime="text/plain",
            )

        except Exception as e:
            st.error("Something went wrong while generating the itinerary.")

            with st.expander("Show error details"):
                st.exception(e)