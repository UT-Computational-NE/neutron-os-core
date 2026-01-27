# Questionnaire_Experiments - Nick and Khiloni Reviewed.pdf

**Extracted:** 2026-01-22 14:41
**Author:** python-docx
**Pages:** 6

---

## 📄 Document Content

### Page 1

Experiment & Sample Tracking 
Questionnaire 
For Research Operations 
Context 
We are building a unified data platform for NETL that includes experiment and sample 
tracking capabilities. The goal is to digitize the workflow from sample preparation through 
irradiation, decay, counting, and analysis. 
Nick Luciano has provided an initial list of sample metadata fields (shown below). We need 
your input to validate this list, understand current workflows, and identify any integration 
needs with scheduling systems. 
Proposed Sample Metadata Fields (from Nick) 
Nick suggested tracking the following for each sample: 
• Sample Name (must be unique) 
• Sample numeric ID (assigned automatically) 
• Chemical Composition 
• Isotopic Composition 
• Density 
• Mass 
• Location of Irradiation (central thimble, lazy susan, etc.) 
• Irradiation Facility (cadmium covered, etc.) 
• Datetime of insertion 
• Datetime of removal 
• Decay time after removal 
• Count Live time 
• Total counts 
• Total activity 
• Activity by isotope 
• Measurement raw data (spectra or other) 
 
Commented [KS1]: What is the purpose of digitizing the 
workflow? Is this to benefit researchers doing similar 
experiments at NETL?  
Commented [LN2R1]: Some benefit to researchers at 
NETL, but can also provide validation data to digital twin 
work. 
Commented [SK3R1]:  
Commented [KS4]: What do you mean by this? Do you 
mean solid/liquid/gas? Or something else?  
Commented [LN5R4]: I mean the molecular formula.  
Like caffeine: C8H10N4O2 
Commented [SK6R4]: This might not always be 
available - some of the work we do is unknown NAA 
samples. You might be better off just asking for a 
description of the sample - in terms of solid, liquid, gas.  
Commented [KS7]: I would say this is the same thing - 
irradiation facility name should give you all the 
information. If you really want a separation, I would have 
irradiation facility be things like the central thimble, 3EL, 
etc. and irradiation location be either in-core or ex-core 
Commented [LN8R7]: That's fine. 
Commented [KS9]: I would rename these as follows: 
1.Irradiation date 
2.Irradiation time  
3.Reactor power level 
Commented [LN10R9]: I use datetime in the python 
sense.  This is a data type that captures both the date and 
time. 
Reactor power level is already being captured.   
Commented [KS11]: This can likely be auto calculated 
by subtracting the irradiation date from the count date 
Commented [LN12R11]: While we need a datetime for 
insertion and removal of the sample to match reactor 
behavior, we only need total seconds for decay time and 
count time.  The decay time and the count live time are 
the total integrated time, like 3600s.  So we can't 
subtract.  Even so, I'd rather the user enter decay time 
explicitly, rather than infer it. 
Commented [SK13R11]: Most users subtract the 
irradiation end date from the count start date to get that 
value using Excel. I'm not sure I understand what you 
mean by total integrated time.  
Commented [KS14]: This is typically post-processing 
information and is usually kept by the researcher to 
analyze the data for whatever they’re doing. It is not 
...
Commented [KS15R14]: You’ll also want to include the 
count datetime in addition to the livetime here if you are ...
Commented [LN16R14]: Regarding data kept by the 
experimenter and not recorded, we are hoping to offer ...
Commented [SK17R14]: If you're offering web 
calculators, you'll need to offer them for all the different ...

### Page 2

Questions 
Question 1 
How are experiments and samples currently tracked? 
Context: We want to understand the current workflow to ensure the new system improves 
rather than disrupts existing processes. 
Follow-up: Is it spreadsheets, paper logs, a database, or ad-hoc? Can you share an example 
of current tracking (redacted if needed)? 
Your Answer: 
It’s a combination of things. Some information – sample type (i.e., solid, liquid, gas), sample 
mass, maximum reactor power you might need (note this is not always what you irradiate 
at), irradiation time, facility, in-core/ex-core, etc. are recorded in reactor operations 
requests. However, depending on the irradiation you’re doing, typically you include a 
variety of things you might do with that ops request so that it can follow cover more than 
one type of experiment. Especially for things like neutron activation analysis – that one 
covers a wide array of samples, sizes, etc. The ops requests also define expected doses from 
samples and any hazards (e.g., gamma emitter, beta emitter, fission product, etc.). Any 
fissioning samples we irradiate (e.g., uranium, plutonium, etc.) go through additional 
calculations to make sure we don’t exceed our technical specifications limits for iodine and 
samarium. If you’re using an ops request for multiple experiments, you’re likely keeping 
track of the experiment details on your own – this can vary widely from person to person – 
spreadsheet, handwritten, etc.  
During irradiations, each facility location has a binder that allows you to write in some 
information – date, time, researcher doing experiment, reactor power level, facility (if more 
than one is available at the location), dose rate – this is only used to record the dose rate of 
the sample when it is done being irradiated.  
For post-processing data analysis, this is also researcher dependent and experiment 
dependent. Some things are done for customers, so we don’t care about anything other than 
a rough estimate of what we produced before we ship it to them. In-house experiments for 
students or staff are typically analyzed in some way – that depends on the sample and what 
it emits. The way the data is analyzed depends on the researcher, but the most common is 
probably some type of spreadsheet.  
Question 2 
Are the metadata fields Nick listed above complete and accurate? 
Context: Nick provided this list based on his understanding. We want to make sure nothing 
is missing and the field names match your terminology. 
Follow-up: Are there fields to add? Remove? Rename? Are some fields optional vs. required?

### Page 3

Your Answer: 
I left comments on the metadata fields directly for thoughts that I had. I don’t see anything 
that needs to be added. Is there a reason you want the post-processing sample information 
as well?  
 
Question 3 
Should the system integrate with a scheduling/calendar system? 
Context: Nick noted that a calendar shows intent (what was planned) while the tracking 
system should show what actually happened. However, linking them could be useful. 
Follow-up: Do you currently use a shared calendar for scheduling reactor time? Would it be 
helpful to see scheduled vs. actual in one view? 
Your Answer: 
The way we schedule reactor time right now is send a calendar request to NETL-Reactor 
with our name, desired power level, estimated irradiation time, facility, and any details that 
might be important to the staff. They will then review that calendar invite and either accept 
or decline it.  
Here’s an example from this week:  
 
I don’t think it actually matters to any of us experimenters what the schedule says – we 
typically write down what happens on the day of for our own purposes and note down any 
changes that may have occurred. For example, when I was doing my PhD research, I used to 
request 8 hours of reactor time at 900 kW. But each time I did an experiment, I would note 
down the start time and the stop time – and also if I ever stopped early or did a shortened 
experiment.

### Page 4

Some requests – typically the pneumatic facility requests – are requested for longer periods 
of time, but actual irradiations are shorter or they do multiple irradiations in the timespan. 
For something like the TPNT/EPNT, you typically request a couple hours and then shoot 
multiple samples for a desired time (usually between 10 seconds and 10 minutes).  
 
Question 4 
What irradiation locations and facilities should be pre-populated? 
Context: Nick suggested pre-populating dropdown menus for common options to speed 
data entry and ensure consistency. 
Follow-up: Can you provide a complete list of: (a) irradiation locations (central thimble, lazy 
susan positions, etc.), and (b) facility configurations (cadmium covered, bare, etc.)? 
Your Answer: 
Ex-core: 
1. Beam Port 1 
2. Beam Port 2 
3. Beam Port 3 
4. Beam Port 4 
5. Beam Port 5 
In-core: 
1. TPNT (thermal pneumatic facility) 
2. EPNT (epithermal pneumatic facility) 
3. RSR (rotary specimen rack) – this technically sits outside the reflector so it might be 
considered ex-core – but we usually call it in-core since it’s inside the pool 
4. CT (central thimble) 
5. F3EL (fast 3-element facility)  
6. 3EL(Cd) (Cd-lined 3-element facility) 
7. 3EL(Pb) (Pb-lined 3-element facility) 
I think that’s all the facilities we have, but you’ll probably want someone on the reactor staff 
to look this over. They’ll know better than me. I’ve combined (a) and (b) in that list because 
that’s how we always define these facilities – I don’t think there’s a need to separate them 
out. They’re all unique facilities.  
Question 5 
What is the typical sample workflow from start to finish? 
Context: Understanding the full lifecycle helps us design a system that supports each step.

### Page 5

Follow-up: Walk us through a typical sample: preparation → approval → insertion → 
irradiation → removal → decay → counting → analysis → disposal. What happens at each 
step? 
Your Answer: 
I would say this depends on the type of experiment happening and whether it’s the first 
time we’re doing something or if we’ve done it multiple times.  
First time experiments have to do a complete safety analysis report and experiment 
authorization form before they can even do an ops request to run a sample. In some cases it 
also requires ROC approval if it is making major changes to the reactor. We have most 
recently done this for the cryo facility in BP2 and the F3EL. If you want more details on that 
I would recommend reaching out to Clayton Hudson – he did the cryo facility analysis.  
If we’re talking about a more general experiment, typically you’ll go as follows: 
1. Create an operations request 
a. Run models (usually analytical or SCALE) to estimate the sample activities – 
go for conservative estimates (it’s better for your sample to be slightly lower 
in activity than slightly higher). The modeling tells you what power 
levels/times you want to target for your irradiation to get a desired activity 
level.  
b. Convert activities to dose rates – the reactor staff don’t usually care about 
activity, they want to know how much beta and gamma dose they will 
receive handling these samples.  
c. If you already have an operations request (noted with a 4-digit number – 
e.g., 1996 in the example I showed a couple questions ago), then you can 
reference that in your calendar request.  
2. Create a calendar request – include name, power level, facility, 4-digit ops request, 
sample, irradiation time. The staff will review and approve.  
3. On irradiation day – the staff will insert the appropriate facilities as needed or for 
ex-core experiments, you will set up your sample and let them know when you’re 
ready. After they’ve completed start up checks, they will turn the reactor on, and 
you can begin your irradiation. During irradiation, experimenters will note down 
anything significant that may have occurred – they will also note down start time 
and stop time if they’re doing longer irradiations. They also record the dose of the 
sample when it is finished being irradiated using a yellow frisker.  
4. After irradiation, samples are pulled – when they are pulled depends on how hot 
they are and when they need to be analyzed/sent off. The medical isotope work we 
do is allowed to decay a little but pulled when still hot because it is a time sensitive 
project. This is something that is decided between the reactor staff and 
experimenter.  
5. Analysis is heavily experimenter dependent – as part of our initial calculations we 
will determine when we need to count a sample and for how long. Some things can

### Page 6

be or need to be counted right away; other things have to decay first. Either way, 
you’ll request the detector time you need or set up your own detectors for analysis. 
Anyways, most commonly, once you are ready to count your sample you will set it 
up on a detector and count it. You will do the respective energy and efficiency 
calibrations for your detectors as well.  
6. Analysis is done in a variety of ways – whatever software you prefer for reading 
spectra. There’s not a specific timeline for analysis – people do it whenever they 
need to – it doesn’t have to be right away.  
7. Disposal is done at the behest of the staff – usually when storage locations get too 
full. Again, this depends on the experiment – long-term experiments usually don’t 
want to get rid of previously irradiated samples until the full project is complete. 
Some things can stay hot for a while and thus can’t get disposed of for a while.  
 
Additional Comments 
Please add any other requirements, concerns, or suggestions for experiment tracking: 
____________________________________________________________ 
____________________________________________________________ 
____________________________________________________________ 
____________________________________________________________ 
 
Thank you for your input! Please return this questionnaire to Ben. 
Contact: bdb3732@utexas.edu
