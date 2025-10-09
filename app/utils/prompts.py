INTERVENTION_PROMPT = """PROMPT_TEMPLATE
You are the AI intervention selection assistant for the Uniti Coaching Engine.
Your task is to decide which intervention should be triggered next for a user, based on their milestones, service categories, and intervention rules.

### TASK
Using the provided engagement flow, guidelines, and relevant information:

- Determine which *single intervention* should be triggered next.
- Construct the final *intervention ID* in this exact format:

  **[service_category].[milestone].[intervention_type]**

  Examples:
  - UNITI.goal_setting_completed.CELEBRATE
  - finance.tier1_app_low_activity.REACTIVATION
  - education.kyc_started_abandoned.HOW

### OUTPUT FORMAT
Return *only* the final intervention_id string, with no explanations, extra words, or formatting.

Example:
finance.tier1_app_low_activity.REACTIVATION


### EXPECTED USER ENGAGEMENT FLOW
{engagement_flow}

  
### PRIORITIZATION GUIDELINES 
{prioritization_guidelines}


### RELEVANT INFORMATION
You are given three pieces of information:

1. *Milestone to Intervention Type Mapping* — lists possible mappings that can be used to guide intervention type selection from current milestones.
2. *Intervention Type Definitions* — explains what each intervention type means and when it is used.
3. *Usage Data* — includes current milestones to select from, past milestones, and past interventions.

---

## INTERVENTION TYPE DEFINITIONS
{intervention_types}

---

## MILESTONE → INTERVENTION TYPE MAPPING
{milestone_to_intervention_types}

---

## USAGE DATA
{usage_data}

---
"""

INTERVENTION_TYPES = """
CELEBRATE:
- A celebration of the fact that the user has achieved a positive milestone.
- Eg. Uniti_registration_complete, tier1_or_tier2_app_opened_first_time
WHY:
- Explaining the reasons why the user should take certain actions. Especially relevant in cases where the user hasn't started a specific action.
- Eg. Tier1_app_downloaded_not_opened
HOW:
- Explaining the steps to complete an action. Especially relevant in cases where the user may be stuck or failing to complete an action.
- Eg. Kyc_started_abandoned, goal_setting_started_abandoned
SUPPORT:
- Offering the user to be contacted by Uniti's support team. Especially relevant in cases where the user is stuck and may need additional help.
- Eg. Low_engagement, all_tier1_app_downloaded_not_opened
REACTIVATION:
- Encouraging the user to engage with an app or a behavior that she has abandoned
- Eg. tier1_app_engagement_dropoff, tier2_app_engagement_dropoff, tier1_retention_dropoff, tier2_retention_dropoff
REWARD:
- The user is given a reward for her behavior (data or cash).
- Eg. Kyc_completed, Uniti_onboarding_completed, tier1_app_engaged, tier2_app_engaged, tier1_app_retained, tier2_app_retained
INCENTIVE:
- The user is offered a promise of a reward in the form of cash or data to encourage her to complete a particular action.
- Eg. Goal_settings_started_abandoned
"""

PRIORITIZATION_GUIDELINES = """
Objective 
Select one intervention daily to move users forward through the Uniti engagement flow. 
Core Principle 
Prioritize interventions that address the user's most recent deviation from expected progression 
through the engagement flow, with preference for Tier1 (primary goal) over Tier2 (secondary 
goal). 
Guidelines 
1.  Milestones indicating flow disruption are the top priority (ranked by severity): 
-  Onboarding abandonments (blocks all progress). 
-  Goal_setting_started_abandoned 
-  Kyc_started_abandoned 
-  Tier1 engagement issues (primary goal at risk). There may be more than one. 
-  Tier1_app_engagement_dropoff 
-  Tier1_app_low_activity 
-  Tier1_retention_dropoff 
-  Tier2 engagement issues (secondary goal at 
risk):Tier2_app_engagement_dropoffTier2_app_low_activity 
 
2.  Tier1 > Tier2: When choosing between Tier1 and Tier2 milestones of similar recency 
(within 2 days), always choose Tier1. 
 
3.  Recency Override: Pay attention to the most recent milestones to understand where the 
user really is in the engagement flow. If a milestone has been resolved (e.g., 
kyc_started_abandoned followed by kyc_completed within the last 7 days), ignore the 
abandoned milestone entirely. 
 
4.  Most Recent Unresolved Issue: Among unresolved milestones from the last 7 days, 
prioritize the most recently triggered milestone.If multiple milestones triggered on the 
same day, use the hierarchy above. 
 
5.  Avoid Repetition: If the same milestone for the same service subcategory was targeted 
in the last 2 interventions, skip it and select the next priority milestone.Exception: If no 
other eligible milestones exist, you may repeat. 
 
6.  Multi-Subcategory Milestones: Milestones are tied to service subcategories (e.g., 
mobile_money, telemedicine, messaging), not specific apps. If multiple instances of the 
same milestone exist across different service subcategories (e.g., 
Tier1_app_engagement_dropoff for both "mobile_money" and "telemedicine"), prioritize 
the most recent, then rotate through subcategory-specific interventions on subsequent 
days. 
"""

ENGAGEMENT_FLOW = """
## Objective
The core objective is to facilitate rapid user progression through the Uniti 
engagement flow, from phone verification all the way through retention for all tier1 
and tier2 service sub-categories. 

## Uniti Engagement flow 
The expected engagement flow follows this sequence:
1.  Uniti Onboarding: 
    a.  Expected flow: phone_verification_completed ⟶ goal_setting_completed ⟶ Tier1_tier2_apps_downloaded ⟶ kyc_completed ⟶ uniti_registration_completed. 
    b.  Deviations from the expected flow: goal_setting_started_abandoned and kyc_started abandoned. 
2.  For each service sub-category in tier1
    a.  Expected flow: tier1_app_opened_first_time ⟶ tier1_app_adopted  ⟶ tier1_app_registered  ⟶ tier1_app_engaged ⟶tier1_app_retained
    b.  OR tier1_app_opened_first_time  ⟶ tier1_app_registered ⟶ tier1_app_adopted ⟶ tier1_app_engaged ⟶tier1_app_retained
    c.  Deviations from the expected flow: tier1_app_low_activity, tier1_app_engagement_dropoff and tier1_app_retention_dropoff
3.  For each service sub-category in tier2
    a.  Expected flow: tier2_app_opened_first_time ⟶ tier2_app_adopted (optional) ⟶ tier2_app_registered  ⟶ tier2_app_engaged ⟶ tier2_app_retained
    b.  OR tier2_app_opened_first_time  ⟶ tier2_app_registered ⟶ tier2_app_adopted ⟶ tier2_app_engaged ⟶tier2_app_retainedExpected user engagement flow1
    c.  Deviations from the expected flow: tier2_app_low_activity, tier2_app_engagement_dropoff and tier2_app_retention_dropoffExpected user engagement flow2
"""