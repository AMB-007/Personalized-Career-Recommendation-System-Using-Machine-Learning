/* ============================================================
   assessment.js - Adaptive Multi-Step AI Career Assessment
   Fully adaptive: Class 7 through Professional Degree
   ============================================================ */

/* -- EDUCATION LEVEL CLASSIFIER -------------------------------- */
function getEduCategory(level) {
  if (["Class 7","Class 8","Class 9","Class 10"].includes(level)) return "class7to10";
  if (level === "Higher Secondary (11-12)") return "higherSecondary";
  if (level === "Diploma / ITI") return "diploma";
  if (level === "Undergraduate") return "ug";
  if (level === "Postgraduate") return "pg";
  if (level === "Professional Degree") return "professional";
  return "ug";
}

function getAptitudeConfig(category) {
  const configs = {
    class7to10:      { total: 5,  easy: 3, medium: 2, hard: 0 },
    higherSecondary: { total: 5,  easy: 2, medium: 2, hard: 1 },
    diploma:         { total: 5,  easy: 2, medium: 2, hard: 1 },
    ug:              { total: 10, easy: 3, medium: 4, hard: 3 },
    pg:              { total: 10, easy: 2, medium: 4, hard: 4 },
    professional:    { total: 10, easy: 2, medium: 3, hard: 5 },
  };
  return configs[category] || configs.ug;
}

function getPsychCount(category) {
  return ["ug","pg","professional"].includes(category) ? 6 : 4;
}

/* -- APTITUDE QUESTION BANK ------------------------------------ */
const APTITUDE_BANK = {

  class7to10: {
    easy: [
      { id:"c7e1",  question_text:"What is the next number in the series: 2, 4, 6, 8, ?", option_a:"9", option_b:"10", option_c:"12", option_d:"11", correct_answer:"B", category:"Number Series", difficulty:"Easy" },
      { id:"c7e2",  question_text:"If 24 chocolates are shared equally among 6 friends, how many does each get?", option_a:"3", option_b:"4", option_c:"6", option_d:"5", correct_answer:"B", category:"Basic Arithmetic", difficulty:"Easy" },
      { id:"c7e3",  question_text:"Which shape has 4 equal sides and 4 right angles?", option_a:"Rectangle", option_b:"Triangle", option_c:"Square", option_d:"Circle", correct_answer:"C", category:"Spatial Reasoning", difficulty:"Easy" },
      { id:"c7e4",  question_text:"Find the odd one out: Dog, Cat, Eagle, Cow, Horse", option_a:"Dog", option_b:"Eagle", option_c:"Cat", option_d:"Horse", correct_answer:"B", category:"Classification", difficulty:"Easy" },
      { id:"c7e5",  question_text:"Book is to Reading as Fork is to ?", option_a:"Kitchen", option_b:"Eating", option_c:"Cooking", option_d:"Spoon", correct_answer:"B", category:"Analogy", difficulty:"Easy" },
      { id:"c7e6",  question_text:"What is 25% of 80?", option_a:"15", option_b:"25", option_c:"20", option_d:"30", correct_answer:"C", category:"Percentage", difficulty:"Easy" },
      { id:"c7e7",  question_text:"A square has side 5 cm. What is its perimeter?", option_a:"10 cm", option_b:"25 cm", option_c:"15 cm", option_d:"20 cm", correct_answer:"D", category:"Geometry", difficulty:"Easy" },
      { id:"c7e8",  question_text:"Which number comes between 15 and 17?", option_a:"14", option_b:"18", option_c:"16", option_d:"13", correct_answer:"C", category:"Basic Arithmetic", difficulty:"Easy" },
      { id:"c7e9",  question_text:"Complete: ABA, BCB, CDC, ?", option_a:"DED", option_b:"DEF", option_c:"EDE", option_d:"DDE", correct_answer:"A", category:"Pattern", difficulty:"Easy" },
      { id:"c7e10", question_text:"A bag has 3 red balls and 2 blue balls. What fraction are red?", option_a:"2/5", option_b:"3/5", option_c:"3/2", option_d:"1/2", correct_answer:"B", category:"Fractions", difficulty:"Easy" },
      { id:"c7e11", question_text:"Pen is to Writer as Brush is to ?", option_a:"Canvas", option_b:"Painter", option_c:"Color", option_d:"Art", correct_answer:"B", category:"Analogy", difficulty:"Easy" },
      { id:"c7e12", question_text:"Which is largest: 1/2, 1/3, 1/4, 1/5?", option_a:"1/3", option_b:"1/4", option_c:"1/5", option_d:"1/2", correct_answer:"D", category:"Fractions", difficulty:"Easy" },
      { id:"c7e13", question_text:"Find the pattern: 5, 10, 15, 20, ?", option_a:"22", option_b:"30", option_c:"25", option_d:"28", correct_answer:"C", category:"Number Series", difficulty:"Easy" },
      { id:"c7e14", question_text:"A clock shows 3:00. What angle does the minute hand make with 12?", option_a:"180 degrees", option_b:"90 degrees", option_c:"270 degrees", option_d:"360 degrees", correct_answer:"B", category:"Spatial Reasoning", difficulty:"Easy" },
      { id:"c7e15", question_text:"How many months have exactly 30 days?", option_a:"3", option_b:"5", option_c:"6", option_d:"4", correct_answer:"D", category:"General Reasoning", difficulty:"Easy" },
    ],
    medium: [
      { id:"c7m1",  question_text:"A shopkeeper has 48 mangoes. Sells 1/4 in morning and 1/3 in evening. How many are left?", option_a:"20", option_b:"16", option_c:"18", option_d:"22", correct_answer:"A", category:"Fractions", difficulty:"Medium" },
      { id:"c7m2",  question_text:"Next in series: 1, 4, 9, 16, 25, ?", option_a:"30", option_b:"36", option_c:"35", option_d:"49", correct_answer:"B", category:"Number Series", difficulty:"Medium" },
      { id:"c7m3",  question_text:"If Monday is day 2, what day number is Sunday?", option_a:"6", option_b:"1", option_c:"8", option_d:"7", correct_answer:"D", category:"Logical Reasoning", difficulty:"Medium" },
      { id:"c7m4",  question_text:"Train leaves 9:45 AM, arrives 1:15 PM. How long is the journey?", option_a:"3 hr 15 min", option_b:"3 hr 30 min", option_c:"4 hr", option_d:"3 hr 45 min", correct_answer:"B", category:"Time", difficulty:"Medium" },
      { id:"c7m5",  question_text:"Find the missing number: 3, 6, 11, 18, 27, ?", option_a:"38", option_b:"36", option_c:"40", option_d:"42", correct_answer:"A", category:"Number Series", difficulty:"Medium" },
      { id:"c7m6",  question_text:"A rectangle has area 36 sq cm, width 4 cm. What is its length?", option_a:"8 cm", option_b:"9 cm", option_c:"6 cm", option_d:"12 cm", correct_answer:"B", category:"Geometry", difficulty:"Medium" },
      { id:"c7m7",  question_text:"Which does NOT belong: 2, 4, 6, 9, 12, 14", option_a:"4", option_b:"9", option_c:"12", option_d:"6", correct_answer:"B", category:"Classification", difficulty:"Medium" },
      { id:"c7m8",  question_text:"Ravi is taller than Sam but shorter than Priya. Who is tallest?", option_a:"Sam", option_b:"Ravi", option_c:"All same", option_d:"Priya", correct_answer:"D", category:"Logical Reasoning", difficulty:"Medium" },
      { id:"c7m9",  question_text:"If today is Wednesday, what day was it 10 days ago?", option_a:"Sunday", option_b:"Saturday", option_c:"Monday", option_d:"Thursday", correct_answer:"A", category:"Logical Reasoning", difficulty:"Medium" },
      { id:"c7m10", question_text:"What fraction of one hour is 20 minutes?", option_a:"1/4", option_b:"1/2", option_c:"1/3", option_d:"2/5", correct_answer:"C", category:"Fractions", difficulty:"Medium" },
      { id:"c7m11", question_text:"A number is doubled and 5 added. Result is 21. What is the number?", option_a:"7", option_b:"8", option_c:"9", option_d:"6", correct_answer:"B", category:"Basic Algebra", difficulty:"Medium" },
      { id:"c7m12", question_text:"Complete: ZA, YB, XC, WD, ?", option_a:"VE", option_b:"UF", option_c:"VF", option_d:"WE", correct_answer:"A", category:"Pattern", difficulty:"Medium" },
      { id:"c7m13", question_text:"Box has 5 red, 3 green, 2 blue pens. Probability of picking green?", option_a:"3/5", option_b:"3/10", option_c:"1/3", option_d:"1/5", correct_answer:"B", category:"Probability", difficulty:"Medium" },
      { id:"c7m14", question_text:"3 notebooks cost Rs.45. How much do 7 cost?", option_a:"Rs.100", option_b:"Rs.95", option_c:"Rs.105", option_d:"Rs.110", correct_answer:"C", category:"Ratio", difficulty:"Medium" },
      { id:"c7m15", question_text:"Average of 12, 18, 24, 30 is?", option_a:"18", option_b:"20", option_c:"21", option_d:"24", correct_answer:"C", category:"Averages", difficulty:"Medium" },
    ],
    hard: []
  },

  higherSecondary: {
    easy: [
      { id:"hse1",  question_text:"What is 15% of 360?", option_a:"54", option_b:"48", option_c:"56", option_d:"60", correct_answer:"A", category:"Percentage", difficulty:"Easy" },
      { id:"hse2",  question_text:"Doctor : Hospital :: Teacher : ?", option_a:"Student", option_b:"School", option_c:"Book", option_d:"Classroom", correct_answer:"B", category:"Analogy", difficulty:"Easy" },
      { id:"hse3",  question_text:"Find odd one out: 36, 49, 64, 81, 100, 112", option_a:"81", option_b:"100", option_c:"112", option_d:"64", correct_answer:"C", category:"Classification", difficulty:"Easy" },
      { id:"hse4",  question_text:"Complete: AZ, BY, CX, DW, ?", option_a:"EV", option_b:"EU", option_c:"FV", option_d:"EW", correct_answer:"A", category:"Pattern", difficulty:"Easy" },
      { id:"hse5",  question_text:"Car covers 150 km in 3 hours. Speed in km/h?", option_a:"40", option_b:"45", option_c:"50", option_d:"55", correct_answer:"C", category:"Speed", difficulty:"Easy" },
      { id:"hse6",  question_text:"What is the next number: 2, 6, 12, 20, 30, ?", option_a:"40", option_b:"42", option_c:"44", option_d:"46", correct_answer:"B", category:"Number Series", difficulty:"Easy" },
      { id:"hse7",  question_text:"If 5x = 35, what is x?", option_a:"5", option_b:"6", option_c:"7", option_d:"8", correct_answer:"C", category:"Algebra", difficulty:"Easy" },
      { id:"hse8",  question_text:"Which word does NOT belong: Mango, Apple, Carrot, Banana, Grapes", option_a:"Mango", option_b:"Carrot", option_c:"Apple", option_d:"Banana", correct_answer:"B", category:"Classification", difficulty:"Easy" },
      { id:"hse9",  question_text:"Pipe fills tank in 10 hours. Fraction filled in 4 hours?", option_a:"2/5", option_b:"1/3", option_c:"3/5", option_d:"4/9", correct_answer:"A", category:"Fractions", difficulty:"Easy" },
      { id:"hse10", question_text:"Complete: 1, 1, 2, 3, 5, 8, 13, ?", option_a:"18", option_b:"19", option_c:"20", option_d:"21", correct_answer:"D", category:"Number Series", difficulty:"Easy" },
    ],
    medium: [
      { id:"hsm1",  question_text:"Shopkeeper buys for Rs.800 and sells at 25% profit. Selling price?", option_a:"Rs.1000", option_b:"Rs.900", option_c:"Rs.1100", option_d:"Rs.1050", correct_answer:"A", category:"Profit & Loss", difficulty:"Medium" },
      { id:"hsm2",  question_text:"Car travels 60 km in 1.5 hours. Speed in m/s?", option_a:"11.11 m/s", option_b:"16.67 m/s", option_c:"10 m/s", option_d:"40 m/s", correct_answer:"A", category:"Speed", difficulty:"Medium" },
      { id:"hsm3",  question_text:"A is 2 years older than B who is twice as old as C. Total = 27. How old is B?", option_a:"8", option_b:"10", option_c:"12", option_d:"9", correct_answer:"B", category:"Age Problems", difficulty:"Medium" },
      { id:"hsm4",  question_text:"Ratio of boys to girls is 3:4. 28 students total. How many boys?", option_a:"10", option_b:"12", option_c:"16", option_d:"14", correct_answer:"B", category:"Ratio", difficulty:"Medium" },
      { id:"hsm5",  question_text:"Find next: 3, 6, 11, 18, 27, ?", option_a:"36", option_b:"38", option_c:"40", option_d:"42", correct_answer:"B", category:"Number Series", difficulty:"Medium" },
      { id:"hsm6",  question_text:"Probability of drawing a red card from a 52-card deck?", option_a:"1/4", option_b:"1/3", option_c:"1/2", option_d:"1/13", correct_answer:"C", category:"Probability", difficulty:"Medium" },
      { id:"hsm7",  question_text:"Clock shows 3:45. What time does mirror image show?", option_a:"8:15", option_b:"9:15", option_c:"8:45", option_d:"9:45", correct_answer:"A", category:"Spatial Reasoning", difficulty:"Medium" },
      { id:"hsm8",  question_text:"12% of 650?", option_a:"78", option_b:"82", option_c:"70", option_d:"84", correct_answer:"A", category:"Percentage", difficulty:"Medium" },
      { id:"hsm9",  question_text:"Room 12m x 9m. Cost to tile at Rs.45 per sq.m?", option_a:"Rs.4860", option_b:"Rs.4500", option_c:"Rs.5040", option_d:"Rs.5400", correct_answer:"A", category:"Area", difficulty:"Medium" },
      { id:"hsm10", question_text:"A invested Rs.5000 for 2 years at 8% simple interest. Total amount?", option_a:"Rs.5400", option_b:"Rs.5600", option_c:"Rs.5800", option_d:"Rs.6000", correct_answer:"C", category:"Finance", difficulty:"Medium" },
    ],
    hard: [
      { id:"hsh1",  question_text:"Pipe fills tank in 6 hours, another empties in 9 hours. Time to fill if both open?", option_a:"12 hrs", option_b:"15 hrs", option_c:"18 hrs", option_d:"9 hrs", correct_answer:"C", category:"Pipes & Cisterns", difficulty:"Hard" },
      { id:"hsh2",  question_text:"Avg of 40 students is 72. If 4 leave with avg 60, new average?", option_a:"73.3", option_b:"72.8", option_c:"74.1", option_d:"71.5", correct_answer:"A", category:"Averages", difficulty:"Hard" },
      { id:"hsh3",  question_text:"If 5 machines make 5 items in 5 minutes, how long for 100 machines to make 100 items?", option_a:"100 min", option_b:"50 min", option_c:"5 min", option_d:"10 min", correct_answer:"C", category:"Logical Reasoning", difficulty:"Hard" },
      { id:"hsh4",  question_text:"In a row, A is 7th from left and 12th from right. People in the row?", option_a:"18", option_b:"19", option_c:"20", option_d:"21", correct_answer:"A", category:"Arrangement", difficulty:"Hard" },
      { id:"hsh5",  question_text:"Two trains 200m and 300m long approach each other at 60 and 90 km/h. Time to cross?", option_a:"6 sec", option_b:"8 sec", option_c:"10 sec", option_d:"12 sec", correct_answer:"C", category:"Speed", difficulty:"Hard" },
    ]
  },

  diploma: {
    easy: [
      { id:"dpe1",  question_text:"SI unit of electrical current?", option_a:"Volt", option_b:"Watt", option_c:"Ampere", option_d:"Ohm", correct_answer:"C", category:"Technical Knowledge", difficulty:"Easy" },
      { id:"dpe2",  question_text:"Tool used to measure electrical resistance?", option_a:"Voltmeter", option_b:"Ammeter", option_c:"Ohmmeter", option_d:"Wattmeter", correct_answer:"C", category:"Technical Knowledge", difficulty:"Easy" },
      { id:"dpe3",  question_text:"How many sides does a hexagon have?", option_a:"5", option_b:"6", option_c:"7", option_d:"8", correct_answer:"B", category:"Spatial Reasoning", difficulty:"Easy" },
      { id:"dpe4",  question_text:"Gear with 40 teeth meshes with 20-tooth gear. Larger turns at 100 RPM. Smaller speed?", option_a:"100 RPM", option_b:"150 RPM", option_c:"200 RPM", option_d:"50 RPM", correct_answer:"C", category:"Technical Reasoning", difficulty:"Easy" },
      { id:"dpe5",  question_text:"What is 1/4 of 400?", option_a:"80", option_b:"100", option_c:"120", option_d:"60", correct_answer:"B", category:"Arithmetic", difficulty:"Easy" },
      { id:"dpe6",  question_text:"A bolt takes 10 turns to move 20 mm. Pitch (distance per turn)?", option_a:"1 mm", option_b:"2 mm", option_c:"5 mm", option_d:"10 mm", correct_answer:"B", category:"Technical Reasoning", difficulty:"Easy" },
      { id:"dpe7",  question_text:"Carpenter : Wood :: Blacksmith : ?", option_a:"Coal", option_b:"Iron", option_c:"Rubber", option_d:"Stone", correct_answer:"B", category:"Analogy", difficulty:"Easy" },
      { id:"dpe8",  question_text:"Which is NOT a conductor of electricity?", option_a:"Copper", option_b:"Iron", option_c:"Rubber", option_d:"Aluminium", correct_answer:"C", category:"Technical Knowledge", difficulty:"Easy" },
      { id:"dpe9",  question_text:"Area of circle with radius 7 cm? (pi approx 22/7)", option_a:"44 sq cm", option_b:"154 sq cm", option_c:"49 sq cm", option_d:"77 sq cm", correct_answer:"B", category:"Geometry", difficulty:"Easy" },
      { id:"dpe10", question_text:"Efficiency of a machine is 80%. Input = 500 J. Output?", option_a:"400 J", option_b:"450 J", option_c:"500 J", option_d:"350 J", correct_answer:"A", category:"Technical Reasoning", difficulty:"Easy" },
    ],
    medium: [
      { id:"dpm1",  question_text:"Pump moves 500 litres/hr. Time to fill 2000 litre tank?", option_a:"2 hours", option_b:"3 hours", option_c:"4 hours", option_d:"5 hours", correct_answer:"C", category:"Applied Maths", difficulty:"Medium" },
      { id:"dpm2",  question_text:"Ohm's Law: V = 12V, R = 4 ohm. Current?", option_a:"2A", option_b:"3A", option_c:"4A", option_d:"48A", correct_answer:"B", category:"Electrical", difficulty:"Medium" },
      { id:"dpm3",  question_text:"A 3-phase motor runs at 1440 RPM. Synchronous speed is 1500 RPM. Slip?", option_a:"2%", option_b:"4%", option_c:"6%", option_d:"8%", correct_answer:"B", category:"Technical Reasoning", difficulty:"Medium" },
      { id:"dpm4",  question_text:"Which number replaces ?: 2, 4, 8, 16, 32, ?", option_a:"48", option_b:"64", option_c:"60", option_d:"96", correct_answer:"B", category:"Number Series", difficulty:"Medium" },
      { id:"dpm5",  question_text:"Volume of cylinder with radius 5 cm and height 10 cm? (pi=3.14)", option_a:"785 cc", option_b:"1570 cc", option_c:"314 cc", option_d:"628 cc", correct_answer:"A", category:"Geometry", difficulty:"Medium" },
      { id:"dpm6",  question_text:"Worker completes job in 8 days, another in 12 days. Together in?", option_a:"4 days", option_b:"4.8 days", option_c:"5 days", option_d:"6 days", correct_answer:"B", category:"Work & Time", difficulty:"Medium" },
      { id:"dpm7",  question_text:"10 kg block on frictionless surface. Force 50 N applied. Acceleration?", option_a:"0.5 m/s2", option_b:"5 m/s2", option_c:"50 m/s2", option_d:"500 m/s2", correct_answer:"B", category:"Technical Reasoning", difficulty:"Medium" },
      { id:"dpm8",  question_text:"Rectangular plate 4m x 3m, 1m x 1m cut from each corner. Remaining area?", option_a:"8 sq m", option_b:"10 sq m", option_c:"12 sq m", option_d:"7 sq m", correct_answer:"A", category:"Spatial Reasoning", difficulty:"Medium" },
      { id:"dpm9",  question_text:"Beam 6m long has 900 N load at centre. Reaction at each support?", option_a:"450 N", option_b:"900 N", option_c:"300 N", option_d:"600 N", correct_answer:"A", category:"Mechanical Reasoning", difficulty:"Medium" },
      { id:"dpm10", question_text:"Series circuit: R1=4 ohm, R2=6 ohm, V=20V. Current?", option_a:"1A", option_b:"2A", option_c:"3A", option_d:"4A", correct_answer:"B", category:"Electrical", difficulty:"Medium" },
    ],
    hard: [
      { id:"dph1",  question_text:"Shaft transmits 30 kW at 300 RPM. Torque (approx)?", option_a:"955 Nm", option_b:"1000 Nm", option_c:"500 Nm", option_d:"1200 Nm", correct_answer:"A", category:"Mechanical Engineering", difficulty:"Hard" },
      { id:"dph2",  question_text:"Hydraulic press: pistons of area 5 cm2 and 100 cm2. Force on small = 50 N. Force on large?", option_a:"100 N", option_b:"500 N", option_c:"1000 N", option_d:"2000 N", correct_answer:"C", category:"Fluid Mechanics", difficulty:"Hard" },
      { id:"dph3",  question_text:"Bearing failure: 40% lubrication, 25% overload, 35% other. Out of 200, failures from overload?", option_a:"40", option_b:"50", option_c:"60", option_d:"70", correct_answer:"B", category:"Applied Problem Solving", difficulty:"Hard" },
      { id:"dph4",  question_text:"CNC tool feed rate 200 mm/min. Time to machine 50 mm depth at 5 passes?", option_a:"1.25 min", option_b:"2.5 min", option_c:"5 min", option_d:"10 min", correct_answer:"A", category:"Technical Reasoning", difficulty:"Hard" },
      { id:"dph5",  question_text:"Transformer primary: 240V, 200 turns. Secondary: 100 turns. Secondary voltage?", option_a:"48V", option_b:"60V", option_c:"120V", option_d:"480V", correct_answer:"C", category:"Electrical", difficulty:"Hard" },
    ]
  },

  ug: {
    easy: [
      { id:"uge1",  question_text:"A = {1,2,3,4}, B = {3,4,5,6}. A intersect B?", option_a:"{1,2}", option_b:"{3,4}", option_c:"{5,6}", option_d:"{1,2,3,4,5,6}", correct_answer:"B", category:"Set Theory", difficulty:"Easy" },
      { id:"uge2",  question_text:"Simple interest on Rs.5000 for 2 years at 8% per annum?", option_a:"Rs.600", option_b:"Rs.700", option_c:"Rs.800", option_d:"Rs.900", correct_answer:"C", category:"Finance", difficulty:"Easy" },
      { id:"uge3",  question_text:"Mean of 5, 10, 15, 20, 25?", option_a:"12", option_b:"15", option_c:"14", option_d:"16", correct_answer:"B", category:"Statistics", difficulty:"Easy" },
      { id:"uge4",  question_text:"Probability of rolling a 6 on a fair die?", option_a:"1/3", option_b:"1/4", option_c:"1/6", option_d:"1/2", correct_answer:"C", category:"Probability", difficulty:"Easy" },
      { id:"uge5",  question_text:"Binary 1010 in decimal?", option_a:"8", option_b:"10", option_c:"12", option_d:"14", correct_answer:"B", category:"Computer Science", difficulty:"Easy" },
      { id:"uge6",  question_text:"f(x) = 2x + 3. f(5) = ?", option_a:"10", option_b:"13", option_c:"15", option_d:"11", correct_answer:"B", category:"Functions", difficulty:"Easy" },
      { id:"uge7",  question_text:"SQL SELECT statement does what?", option_a:"Inserts data", option_b:"Deletes rows", option_c:"Retrieves data", option_d:"Updates rows", correct_answer:"C", category:"Database", difficulty:"Easy" },
      { id:"uge8",  question_text:"Normal distribution: data within +/-1 std dev?", option_a:"68%", option_b:"95%", option_c:"99%", option_d:"50%", correct_answer:"A", category:"Statistics", difficulty:"Easy" },
    ],
    medium: [
      { id:"ugm1",  question_text:"Bag has 4 red and 6 blue balls. Two drawn without replacement. P(both red)?", option_a:"2/15", option_b:"1/15", option_c:"4/15", option_d:"2/9", correct_answer:"A", category:"Probability", difficulty:"Medium" },
      { id:"ugm2",  question_text:"Time complexity of Binary Search?", option_a:"O(N)", option_b:"O(N log N)", option_c:"O(log N)", option_d:"O(1)", correct_answer:"C", category:"Algorithms", difficulty:"Medium" },
      { id:"ugm3",  question_text:"Compound interest on Rs.10,000 at 10% for 2 years compounded annually?", option_a:"Rs.2000", option_b:"Rs.2100", option_c:"Rs.1900", option_d:"Rs.2200", correct_answer:"B", category:"Finance", difficulty:"Medium" },
      { id:"ugm4",  question_text:"Standard deviation measures?", option_a:"Central tendency", option_b:"Skewness", option_c:"Dispersion", option_d:"Kurtosis", correct_answer:"C", category:"Statistics", difficulty:"Medium" },
      { id:"ugm5",  question_text:"Linked list with n elements. Worst case search time?", option_a:"O(1)", option_b:"O(log n)", option_c:"O(n)", option_d:"O(n^2)", correct_answer:"C", category:"Data Structures", difficulty:"Medium" },
      { id:"ugm6",  question_text:"Survey: 60% like tea, 50% coffee, 30% both. % who like neither?", option_a:"10%", option_b:"15%", option_c:"20%", option_d:"25%", correct_answer:"C", category:"Set Theory", difficulty:"Medium" },
      { id:"ugm7",  question_text:"Current ratio 2:1, current liabilities=Rs.50,000. Current assets?", option_a:"Rs.25,000", option_b:"Rs.50,000", option_c:"Rs.1,00,000", option_d:"Rs.75,000", correct_answer:"C", category:"Accounting", difficulty:"Medium" },
      { id:"ugm8",  question_text:"Normalization in a database prevents?", option_a:"Slow queries", option_b:"Data redundancy", option_c:"Missing data", option_d:"Security issues", correct_answer:"B", category:"Database", difficulty:"Medium" },
      { id:"ugm9",  question_text:"Derivative of x^3 + 2x^2 - 5x + 7 at x=2?", option_a:"11", option_b:"15", option_c:"13", option_d:"17", correct_answer:"B", category:"Calculus", difficulty:"Medium" },
      { id:"ugm10", question_text:"Company revenue grew from 500 to 650 Lakhs. Percentage growth?", option_a:"25%", option_b:"28%", option_c:"30%", option_d:"32%", correct_answer:"C", category:"Business Maths", difficulty:"Medium" },
    ],
    hard: [
      { id:"ugh1",  question_text:"Worst-case time complexity of QuickSort?", option_a:"O(N log N)", option_b:"O(N^2)", option_c:"O(N)", option_d:"O(log N)", correct_answer:"B", category:"Algorithms", difficulty:"Hard" },
      { id:"ugh2",  question_text:"P(A)=0.4, P(B)=0.5, P(A or B)=0.7. P(A and B)?", option_a:"0.1", option_b:"0.2", option_c:"0.3", option_d:"0.4", correct_answer:"B", category:"Probability", difficulty:"Hard" },
      { id:"ugh3",  question_text:"Hash table 10 buckets, division method. Key 127 goes to bucket?", option_a:"7", option_b:"2", option_c:"1", option_d:"3", correct_answer:"A", category:"Data Structures", difficulty:"Hard" },
      { id:"ugh4",  question_text:"Regression y=2x+3. If x increases by 1, y changes by?", option_a:"3", option_b:"5", option_c:"2", option_d:"1", correct_answer:"C", category:"Statistics", difficulty:"Hard" },
      { id:"ugh5",  question_text:"D/E ratio=1.5, Equity=Rs.2 Crore. Total assets?", option_a:"Rs.3 Crore", option_b:"Rs.4 Crore", option_c:"Rs.5 Crore", option_d:"Rs.6 Crore", correct_answer:"C", category:"Finance", difficulty:"Hard" },
      { id:"ugh6",  question_text:"In critical path analysis, slack=0 means the task is?", option_a:"Optional", option_b:"Has buffer", option_c:"On the critical path", option_d:"Completed", correct_answer:"C", category:"Project Management", difficulty:"Hard" },
      { id:"ugh7",  question_text:"NPV=-Rs.10,000 at 10%, +Rs.5,000 at 5%. IRR approximately?", option_a:"7.5%", option_b:"6.67%", option_c:"8%", option_d:"5.5%", correct_answer:"B", category:"Finance", difficulty:"Hard" },
    ]
  },

  pg: {
    easy: [
      { id:"pge1", question_text:"ANOVA stands for?", option_a:"Analysis of Variance", option_b:"Average Number of Values and Averages", option_c:"Analytical Value Notation", option_d:"Associative Numerical Variance", correct_answer:"A", category:"Statistics", difficulty:"Easy" },
      { id:"pge2", question_text:"Overfitting in ML means?", option_a:"Model generalizes well", option_b:"Model memorizes training data and fails on new data", option_c:"Model is too simple", option_d:"Model has too little data", correct_answer:"B", category:"ML Concepts", difficulty:"Easy" },
      { id:"pge3", question_text:"A p-value is?", option_a:"Probability null hypothesis is true", option_b:"Probability of observing result if null hypothesis is true", option_c:"Effect size", option_d:"Statistical power", correct_answer:"B", category:"Statistics", difficulty:"Easy" },
      { id:"pge4", question_text:"Algorithm used for dimensionality reduction?", option_a:"K-Means", option_b:"Random Forest", option_c:"PCA", option_d:"SVM", correct_answer:"C", category:"Data Science", difficulty:"Easy" },
      { id:"pge5", question_text:"Normal distribution: data within +/-1 std dev?", option_a:"68%", option_b:"95%", option_c:"99%", option_d:"50%", correct_answer:"A", category:"Statistics", difficulty:"Easy" },
    ],
    medium: [
      { id:"pgm1", question_text:"Random Forest final prediction for classification is by?", option_a:"Average output", option_b:"Majority voting", option_c:"Best-performing tree", option_d:"Weighted average", correct_answer:"B", category:"Machine Learning", difficulty:"Medium" },
      { id:"pgm2", question_text:"Gradient Descent minimizes a function by moving in which direction?", option_a:"Gradient direction", option_b:"Opposite of gradient direction", option_c:"Random direction", option_d:"Perpendicular to gradient", correct_answer:"B", category:"Optimization", difficulty:"Medium" },
      { id:"pgm3", question_text:"TF-IDF in NLP measures?", option_a:"Topic frequency", option_b:"Importance of a word relative to document and corpus", option_c:"Time-frequency inverse documents", option_d:"Text formatting indicators", correct_answer:"B", category:"NLP", difficulty:"Medium" },
      { id:"pgm4", question_text:"Type II error in research is?", option_a:"Rejecting a true null hypothesis", option_b:"Accepting a false null hypothesis", option_c:"Sample bias", option_d:"Low power", correct_answer:"B", category:"Research Methods", difficulty:"Medium" },
      { id:"pgm5", question_text:"Market demand Q = 100 - 2P. At P=20, price elasticity is?", option_a:"-0.5", option_b:"-0.67", option_c:"-1", option_d:"-1.5", correct_answer:"B", category:"Economics", difficulty:"Medium" },
      { id:"pgm6", question_text:"Internal validity in research refers to?", option_a:"How well results apply outside the study", option_b:"Whether the study measures what it claims to", option_c:"Sample representativeness", option_d:"Statistical significance", correct_answer:"B", category:"Research Methods", difficulty:"Medium" },
      { id:"pgm7", question_text:"Eigenvalue decomposition is mainly used to find?", option_a:"Inverse of a matrix", option_b:"Principal components", option_c:"Determinants", option_d:"Matrix rank", correct_answer:"B", category:"Linear Algebra", difficulty:"Medium" },
      { id:"pgm8", question_text:"Meta-analysis with I2 = 85% indicates?", option_a:"Low heterogeneity", option_b:"Moderate heterogeneity", option_c:"High heterogeneity", option_d:"No heterogeneity", correct_answer:"C", category:"Research Methods", difficulty:"Medium" },
    ],
    hard: [
      { id:"pgh1", question_text:"Markov chain: all eigenvalues of transition matrix < 1 except one = 1. Chain is?", option_a:"Transient", option_b:"Periodic", option_c:"Ergodic/Regular", option_d:"Absorbing", correct_answer:"C", category:"Probability Theory", difficulty:"Hard" },
      { id:"pgh2", question_text:"SEM path: X to Y = 0.3, Y to Z = 0.4. Indirect effect of X on Z?", option_a:"0.12", option_b:"0.7", option_c:"0.1", option_d:"0.34", correct_answer:"A", category:"Research Methods", difficulty:"Hard" },
      { id:"pgh3", question_text:"Vanishing gradient in deep learning is mostly addressed by?", option_a:"Sigmoid activation", option_b:"ReLU + good weight initialization", option_c:"Softmax activation", option_d:"Tanh only", correct_answer:"B", category:"Deep Learning", difficulty:"Hard" },
      { id:"pgh4", question_text:"KL divergence D(P||Q) = 0 means?", option_a:"P and Q are orthogonal", option_b:"P and Q are identical", option_c:"P dominates Q", option_d:"Q dominates P", correct_answer:"B", category:"Information Theory", difficulty:"Hard" },
      { id:"pgh5", question_text:"Hausman test in econometrics is used to choose between?", option_a:"OLS and GLS", option_b:"Fixed effects and Random effects", option_c:"ARIMA and VAR", option_d:"Probit and Logit", correct_answer:"B", category:"Econometrics", difficulty:"Hard" },
      { id:"pgh6", question_text:"KKT conditions are necessary and sufficient for optimality when?", option_a:"Objective is linear", option_b:"Problem is convex and constraint qualification holds", option_c:"Problem is non-convex", option_d:"Only inequality constraints exist", correct_answer:"B", category:"Optimization", difficulty:"Hard" },
      { id:"pgh7", question_text:"In Bayesian inference, the posterior is proportional to?", option_a:"Prior only", option_b:"Likelihood only", option_c:"Prior times Likelihood", option_d:"Marginal likelihood", correct_answer:"C", category:"Bayesian Statistics", difficulty:"Hard" },
    ]
  },

  professional: {
    easy: [
      { id:"pre1", question_text:"Financial statement showing position at a specific date?", option_a:"Income Statement", option_b:"Cash Flow Statement", option_c:"Balance Sheet", option_d:"Retained Earnings", correct_answer:"C", category:"Finance", difficulty:"Easy" },
      { id:"pre2", question_text:"Informed consent in medical practice primarily protects?", option_a:"The hospital", option_b:"The physician", option_c:"Patient autonomy", option_d:"Insurance companies", correct_answer:"C", category:"Professional Ethics", difficulty:"Easy" },
      { id:"pre3", question_text:"A null result in research means?", option_a:"Research was wrong", option_b:"No statistically significant effect found", option_c:"Sample was biased", option_d:"Should not be published", correct_answer:"B", category:"Research", difficulty:"Easy" },
      { id:"pre4", question_text:"Stare decisis in law means?", option_a:"Present new evidence", option_b:"Stand by decided cases - follow precedent", option_c:"Argue against the court", option_d:"Review the statute", correct_answer:"B", category:"Legal Reasoning", difficulty:"Easy" },
      { id:"pre5", question_text:"WACC is used in?", option_a:"HR planning", option_b:"Investment project evaluation", option_c:"Marketing strategy", option_d:"Inventory management", correct_answer:"B", category:"Finance", difficulty:"Easy" },
    ],
    medium: [
      { id:"prm1", question_text:"Competent patient refuses life-saving surgery. Physician should?", option_a:"Override and perform", option_b:"Respect decision, document it", option_c:"Call police", option_d:"Discharge immediately", correct_answer:"B", category:"Medical Ethics", difficulty:"Medium" },
      { id:"prm2", question_text:"Goodwill in a corporate merger represents?", option_a:"Employee satisfaction", option_b:"Excess of purchase price over fair value of net assets", option_c:"Brand advertising", option_d:"Customer loyalty cost", correct_answer:"B", category:"Finance", difficulty:"Medium" },
      { id:"prm3", question_text:"Law firm has conflict of interest if?", option_a:"A lawyer is busy", option_b:"Lawyer represents opposing parties in same matter", option_c:"Client pays late", option_d:"Different jurisdiction involved", correct_answer:"B", category:"Legal Ethics", difficulty:"Medium" },
      { id:"prm4", question_text:"Phase III clinical trial evaluates?", option_a:"Safety in animals", option_b:"Toxicity in small human groups", option_c:"Efficacy and safety in large patient populations", option_d:"Post-market surveillance", correct_answer:"C", category:"Medical Research", difficulty:"Medium" },
      { id:"prm5", question_text:"In tort law, proximate cause means?", option_a:"Defendant was present", option_b:"Harm was foreseeable result of defendant's action", option_c:"Plaintiff suffered no loss", option_d:"Contract was breached", correct_answer:"B", category:"Legal Reasoning", difficulty:"Medium" },
      { id:"prm6", question_text:"Forensic audit differs from statutory audit in that it?", option_a:"Follows accounting standards", option_b:"Is used in legal proceedings to investigate fraud", option_c:"Only audits financial statements", option_d:"Is done annually", correct_answer:"B", category:"Auditing", difficulty:"Medium" },
      { id:"prm7", question_text:"Structural engineer design load includes?", option_a:"Only dead loads", option_b:"Dead + Live + Environmental loads", option_c:"Only live loads", option_d:"Only seismic loads", correct_answer:"B", category:"Engineering", difficulty:"Medium" },
    ],
    hard: [
      { id:"prh1", question_text:"Revenue=500Cr, EBIT=80Cr, Interest=20Cr, Tax=30%, Shares=1Cr. EPS?", option_a:"Rs.42", option_b:"Rs.56", option_c:"Rs.60", option_d:"Rs.35", correct_answer:"A", category:"Financial Analysis", difficulty:"Hard" },
      { id:"prh2", question_text:"Physician faces autonomy vs beneficence dilemma. Best resolved by?", option_a:"Administrative authority", option_b:"Applying four principles of bioethics contextually", option_c:"Legal mandate", option_d:"Institutional policy alone", correct_answer:"B", category:"Medical Ethics", difficulty:"Hard" },
      { id:"prh3", question_text:"DCF terminal value: g=3%, WACC=10%, FCF=Rs.50Cr. Gordon Growth Model TV?", option_a:"Rs.500 Cr", option_b:"Rs.714 Cr", option_c:"Rs.1000 Cr", option_d:"Rs.600 Cr", correct_answer:"B", category:"Valuation", difficulty:"Hard" },
      { id:"prh4", question_text:"Lawyer receives evidence proving opposing party innocent. Obligation?", option_a:"Destroy evidence", option_b:"Use it to settle", option_c:"Disclose to court as exculpatory", option_d:"Keep confidential", correct_answer:"C", category:"Legal Ethics", difficulty:"Hard" },
      { id:"prh5", question_text:"Monte Carlo: 10,000 runs show NPV negative 35% of time. This indicates?", option_a:"35% chance of project failure risk", option_b:"65% chance is guaranteed positive", option_c:"Model is inaccurate", option_d:"No risk at all", correct_answer:"A", category:"Risk Analysis", difficulty:"Hard" },
      { id:"prh6", question_text:"Drug: 2% absolute risk reduction (control=10%, treatment=8%). NNT?", option_a:"2", option_b:"50", option_c:"100", option_d:"10", correct_answer:"B", category:"Medical Statistics", difficulty:"Hard" },
      { id:"prh7", question_text:"Corporate veil is pierced when?", option_a:"Company has losses", option_b:"Corporate form used as sham to perpetrate fraud", option_c:"Company is listed", option_d:"Merger is proposed", correct_answer:"B", category:"Corporate Law", difficulty:"Hard" },
    ]
  }
};

/* -- SELECT APTITUDE QUESTIONS --------------------------------- */
function selectAptitudeQuestions(category) {
  const config = getAptitudeConfig(category);
  const bank = APTITUDE_BANK[category] || APTITUDE_BANK.ug;
  function pickRandom(arr, n) {
    return [...arr].sort(() => Math.random() - 0.5).slice(0, n);
  }
  const easyPick  = pickRandom(bank.easy   || [], config.easy);
  const medPick   = pickRandom(bank.medium  || [], config.medium);
  const hardPick  = pickRandom(bank.hard    || [], config.hard);
  return [...easyPick, ...medPick, ...hardPick].sort(() => Math.random() - 0.5);
}

/* -- PSYCHOMETRIC BANK ----------------------------------------- */
const PSYCH_BANK = {
  class7to10: [
    { q:"When your teacher gives you a difficult homework, what do you usually do?", options:[
      {label:"Try to do it myself first, then ask for help if needed", traits:{Persistence:15, Curiosity:10}},
      {label:"Work with classmates to solve it together", traits:{Teamwork:15, Communication:10}},
      {label:"Look at how similar problems were solved and adapt", traits:{Analytical_Thinking:15, Self_Learning:10}},
      {label:"Ask my teacher or parent for guidance right away", traits:{Communication:10, Adaptability:10}},
    ]},
    { q:"If you had to plan a school event, what role would you most enjoy?", options:[
      {label:"Being the team leader and organizing everyone", traits:{Leadership:15, Communication:10}},
      {label:"Creating the decorations and artwork", traits:{Creativity:15, Curiosity:10}},
      {label:"Managing the schedule and making sure things run on time", traits:{Decision_Making:15, Time_Management:10}},
      {label:"Supporting others and making sure everyone feels included", traits:{Teamwork:15, Adaptability:10}},
    ]},
    { q:"When you play a game and you are losing, what do you usually do?", options:[
      {label:"Keep trying different strategies until one works", traits:{Persistence:15, Problem_Solving:10}},
      {label:"Stay calm and enjoy playing regardless of the score", traits:{Adaptability:15, Confidence:10}},
      {label:"Encourage teammates and figure out why you are losing", traits:{Leadership:10, Analytical_Thinking:15}},
      {label:"Accept the result gracefully and learn from it", traits:{Adaptability:15, Confidence:10}},
    ]},
    { q:"Your friend is having trouble understanding a math problem. You:", options:[
      {label:"Explain it step by step in a simple way", traits:{Communication:15, Teamwork:10}},
      {label:"Work through the problem together until both understand", traits:{Teamwork:15, Persistence:10}},
      {label:"Show them a different way to think about it", traits:{Creativity:15, Analytical_Thinking:10}},
      {label:"Suggest they ask the teacher for extra help", traits:{Communication:10, Decision_Making:10}},
    ]},
    { q:"If you could improve one thing about your school, what would it be?", options:[
      {label:"Better computers and technology for learning", traits:{Curiosity:15, Analytical_Thinking:10}},
      {label:"More art, music and creative activities", traits:{Creativity:15, Curiosity:10}},
      {label:"More sports and outdoor activities", traits:{Teamwork:10, Confidence:10}},
      {label:"Better libraries and reading resources", traits:{Curiosity:15, Self_Learning:10}},
    ]},
    { q:"When assigned a group project at school, you:", options:[
      {label:"Take charge and divide the work fairly", traits:{Leadership:15, Decision_Making:10}},
      {label:"Listen to everyone's ideas before suggesting a plan", traits:{Communication:15, Teamwork:10}},
      {label:"Focus on the most important parts to finish on time", traits:{Time_Management:15, Analytical_Thinking:10}},
      {label:"Make sure every team member is included and happy", traits:{Teamwork:15, Communication:10}},
    ]},
    { q:"You have to speak in front of the whole class. How do you feel?", options:[
      {label:"Excited and eager to share what I know", traits:{Confidence:15, Communication:10}},
      {label:"A bit nervous but I prepare well and do my best", traits:{Persistence:15, Time_Management:10}},
      {label:"I focus on making it interesting with examples", traits:{Creativity:15, Communication:10}},
      {label:"I keep it brief and clear so everyone understands", traits:{Communication:15, Analytical_Thinking:10}},
    ]},
    { q:"You finish your class work early. What do you do?", options:[
      {label:"Read a book or explore something I am curious about", traits:{Curiosity:15, Self_Learning:10}},
      {label:"Help a classmate who is still struggling", traits:{Teamwork:15, Communication:10}},
      {label:"Review my work to check for mistakes", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Start on upcoming assignments to stay ahead", traits:{Time_Management:15, Persistence:10}},
    ]},
    { q:"Your favourite school project would be:", options:[
      {label:"A science experiment to discover something new", traits:{Curiosity:15, Analytical_Thinking:10}},
      {label:"Making a creative story or artwork", traits:{Creativity:15, Confidence:10}},
      {label:"Building or constructing something useful", traits:{Problem_Solving:15, Analytical_Thinking:10}},
      {label:"Organising a charity drive for the community", traits:{Leadership:10, Teamwork:15}},
    ]},
    { q:"When you disagree with a classmate, you:", options:[
      {label:"Calmly explain your point of view", traits:{Communication:15, Confidence:10}},
      {label:"Try to see it from their perspective first", traits:{Adaptability:15, Teamwork:10}},
      {label:"Look for facts or reasons to settle the disagreement", traits:{Analytical_Thinking:15, Decision_Making:10}},
      {label:"Suggest a compromise that works for both", traits:{Teamwork:15, Communication:10}},
    ]},
  ],

  higherSecondary: [
    { q:"You are preparing for board exams and feel overwhelmed. Your approach?", options:[
      {label:"Make a study schedule and stick to it systematically", traits:{Time_Management:15, Persistence:10}},
      {label:"Form a study group with friends to cover topics together", traits:{Teamwork:15, Communication:10}},
      {label:"Identify my weak areas and focus extra time on those", traits:{Analytical_Thinking:15, Self_Learning:10}},
      {label:"Stay calm and remind myself that I can handle the pressure", traits:{Adaptability:15, Confidence:10}},
    ]},
    { q:"You have to choose your stream. You prioritize:", options:[
      {label:"What I am genuinely passionate and curious about", traits:{Curiosity:15, Decision_Making:10}},
      {label:"What will give me the most career options", traits:{Decision_Making:15, Analytical_Thinking:10}},
      {label:"What my strengths and skills align with", traits:{Analytical_Thinking:15, Confidence:10}},
      {label:"What I can contribute meaningfully to society with", traits:{Leadership:10, Teamwork:10}},
    ]},
    { q:"Teacher gives you a challenging assignment with no clear instructions. You:", options:[
      {label:"Research the topic broadly and define my own structure", traits:{Curiosity:15, Self_Learning:10}},
      {label:"Clarify requirements with the teacher before starting", traits:{Communication:15, Decision_Making:10}},
      {label:"Break it into smaller parts and tackle each methodically", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Find similar examples online and adapt them", traits:{Adaptability:15, Curiosity:10}},
    ]},
    { q:"Part of a team preparing a presentation. Most important to you?", options:[
      {label:"The content is accurate and well-researched", traits:{Analytical_Thinking:15, Curiosity:10}},
      {label:"Everyone contributes fairly", traits:{Teamwork:15, Leadership:10}},
      {label:"The delivery is engaging and captures the audience", traits:{Communication:15, Creativity:10}},
      {label:"It is completed on time with no last-minute rush", traits:{Time_Management:15, Persistence:10}},
    ]},
    { q:"A classmate accuses you of copying their answer. You:", options:[
      {label:"Calmly explain that it was coincidental and show your work", traits:{Confidence:15, Communication:10}},
      {label:"Suggest involving the teacher for a fair resolution", traits:{Decision_Making:15, Communication:10}},
      {label:"Feel upset but try to understand their perspective", traits:{Adaptability:10, Teamwork:10}},
      {label:"Present evidence of your own thought process clearly", traits:{Analytical_Thinking:15, Confidence:10}},
    ]},
    { q:"Ideal way to spend a free Saturday afternoon?", options:[
      {label:"Learning a new skill or exploring a topic I am curious about", traits:{Curiosity:15, Self_Learning:10}},
      {label:"Working on a creative project - writing, art or music", traits:{Creativity:15, Persistence:10}},
      {label:"Volunteering or doing something helpful in the community", traits:{Teamwork:10, Leadership:10}},
      {label:"Relaxing but thinking through goals and future plans", traits:{Decision_Making:15, Analytical_Thinking:10}},
    ]},
    { q:"In a class debate you are assigned a position you disagree with. You:", options:[
      {label:"Research it thoroughly and argue it as convincingly as possible", traits:{Analytical_Thinking:15, Communication:10}},
      {label:"Feel uncomfortable but accept it as a learning exercise", traits:{Adaptability:15, Persistence:10}},
      {label:"Find the strongest points in the position and focus on those", traits:{Analytical_Thinking:15, Decision_Making:10}},
      {label:"See it as an opportunity to understand different perspectives", traits:{Curiosity:15, Adaptability:10}},
    ]},
    { q:"When you face failure like a poor test result, what do you do first?", options:[
      {label:"Analyse what went wrong and make a correction plan", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Speak to my teacher or a mentor for guidance", traits:{Communication:10, Adaptability:10}},
      {label:"Give myself a short break and then get back to work", traits:{Adaptability:15, Time_Management:10}},
      {label:"Motivate myself by remembering past successes", traits:{Confidence:15, Persistence:10}},
    ]},
  ],

  diploma: [
    { q:"You are given a technical repair job no one in your workshop has done before. You:", options:[
      {label:"Study the equipment manual and troubleshoot systematically", traits:{Analytical_Thinking:15, Self_Learning:10}},
      {label:"Consult experienced colleagues or call the manufacturer", traits:{Communication:15, Teamwork:10}},
      {label:"Try different approaches carefully until one works", traits:{Persistence:15, Adaptability:10}},
      {label:"Document the problem and break it down step by step", traits:{Analytical_Thinking:15, Persistence:10}},
    ]},
    { q:"Your supervisor asks you to do a task in a way you know is less efficient. You:", options:[
      {label:"Follow instructions but suggest the better method politely", traits:{Communication:15, Confidence:10}},
      {label:"Follow instructions without question", traits:{Adaptability:10, Teamwork:10}},
      {label:"Try prescribed way first then show results with my method", traits:{Decision_Making:15, Analytical_Thinking:10}},
      {label:"Request a meeting to explain the efficiency difference with data", traits:{Communication:15, Leadership:10}},
    ]},
    { q:"You notice a potential safety hazard in your work area. You:", options:[
      {label:"Fix it immediately if I can, then report to supervisor", traits:{Decision_Making:15, Persistence:10}},
      {label:"Report it immediately to the safety officer", traits:{Communication:15, Decision_Making:10}},
      {label:"Warn colleagues nearby and then file a formal report", traits:{Teamwork:15, Communication:10}},
      {label:"Document it carefully with photos and report in writing", traits:{Analytical_Thinking:15, Communication:10}},
    ]},
    { q:"You have to train a new colleague on a complex procedure. You:", options:[
      {label:"Demonstrate once, then let them practice while I supervise", traits:{Leadership:15, Communication:10}},
      {label:"Explain the theory first, then demonstrate practically", traits:{Communication:15, Analytical_Thinking:10}},
      {label:"Give them the manual and let them ask questions as they go", traits:{Adaptability:10, Teamwork:10}},
      {label:"Break it into stages, check understanding at each step", traits:{Time_Management:15, Communication:10}},
    ]},
    { q:"When you make a technical mistake affecting a product, you:", options:[
      {label:"Report it immediately and help identify a fix", traits:{Communication:15, Decision_Making:10}},
      {label:"Analyse how it happened to prevent recurrence", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Take full responsibility and correct it", traits:{Confidence:10, Adaptability:10}},
      {label:"Document the error and corrective action taken", traits:{Analytical_Thinking:15, Persistence:10}},
    ]},
    { q:"Your preferred way to improve technical skills is:", options:[
      {label:"Hands-on practice on real projects", traits:{Persistence:15, Problem_Solving:10}},
      {label:"Taking structured courses or certifications", traits:{Self_Learning:15, Time_Management:10}},
      {label:"Learning from experienced technicians on the job", traits:{Teamwork:15, Curiosity:10}},
      {label:"Reading technical manuals and online documentation", traits:{Curiosity:15, Self_Learning:10}},
    ]},
  ],

  ug: [
    { q:"Your team is behind schedule on a critical college project. What do you do?", options:[
      {label:"Organize a triage meeting and reassign tasks based on capacity", traits:{Leadership:15, Communication:10}},
      {label:"Work extra hours yourself to bridge the gap", traits:{Persistence:15, Self_Learning:10}},
      {label:"Motivate the team and keep morale high", traits:{Teamwork:15, Communication:10}},
      {label:"Prioritize ruthlessly and cut non-essential tasks", traits:{Decision_Making:15, Analytical_Thinking:10}},
    ]},
    { q:"You encounter a completely unfamiliar problem in your coursework. You:", options:[
      {label:"Research methodically using textbooks and online resources", traits:{Curiosity:15, Self_Learning:10}},
      {label:"Ask a senior or faculty member for guidance", traits:{Teamwork:10, Adaptability:10}},
      {label:"Break it into smaller sub-problems and tackle each one", traits:{Analytical_Thinking:15, Problem_Solving:10}},
      {label:"Try different approaches systematically until one works", traits:{Persistence:15, Adaptability:10}},
    ]},
    { q:"You are free to choose a final year project topic. You choose:", options:[
      {label:"The most technically challenging unsolved problem I can find", traits:{Curiosity:15, Analytical_Thinking:10}},
      {label:"Something with clear social impact in my community", traits:{Leadership:10, Communication:10}},
      {label:"Something involving creative design and innovation", traits:{Creativity:15, Self_Learning:10}},
      {label:"Something with strong industry application and job relevance", traits:{Decision_Making:10, Analytical_Thinking:10}},
    ]},
    { q:"Critical bug found 1 hour before software demo submission. You:", options:[
      {label:"Stay calm, assess severity and decide whether to fix or flag it", traits:{Adaptability:15, Decision_Making:10}},
      {label:"Rally the whole team to solve it immediately", traits:{Leadership:15, Teamwork:10}},
      {label:"Apply a quick workaround now and plan proper fix later", traits:{Adaptability:15, Problem_Solving:10}},
      {label:"Inform the client with a clear status and timeline", traits:{Communication:15, Confidence:10}},
    ]},
    { q:"You receive critical feedback on a project you were proud of. You:", options:[
      {label:"Reflect carefully on the feedback and look for truth in it", traits:{Analytical_Thinking:15, Adaptability:10}},
      {label:"Ask for specific examples to better understand the critique", traits:{Communication:15, Curiosity:10}},
      {label:"Defend your decisions but stay open to revision", traits:{Confidence:15, Analytical_Thinking:10}},
      {label:"Thank them and act on the feedback immediately", traits:{Teamwork:10, Adaptability:15}},
    ]},
    { q:"You have to present a complex technical concept to a non-technical audience:", options:[
      {label:"Use simple analogies and real-world examples", traits:{Communication:15, Creativity:10}},
      {label:"Create a visual presentation with diagrams and infographics", traits:{Creativity:15, Analytical_Thinking:10}},
      {label:"Walk them through the logic patiently step by step", traits:{Persistence:10, Communication:15}},
      {label:"Focus on the practical outcomes and benefits", traits:{Leadership:10, Decision_Making:15}},
    ]},
    { q:"You have 3 equally important assignments and time for only 2. You:", options:[
      {label:"Rank by impact and drop the lowest-impact one", traits:{Decision_Making:15, Analytical_Thinking:10}},
      {label:"Try to do all 3 partially to meet all commitments", traits:{Persistence:10, Time_Management:10}},
      {label:"Ask a friend to take over one assignment", traits:{Leadership:15, Teamwork:10}},
      {label:"Communicate the conflict to faculty and ask for guidance", traits:{Communication:15, Confidence:10}},
    ]},
    { q:"Working in a group with people you disagree with, you:", options:[
      {label:"Focus on shared goals and find common ground first", traits:{Teamwork:15, Communication:10}},
      {label:"Propose a structured approach so everyone contributes fairly", traits:{Leadership:15, Decision_Making:10}},
      {label:"Adapt to the group dynamic and find where you contribute best", traits:{Adaptability:15, Teamwork:10}},
      {label:"Listen to all views carefully before proposing a middle path", traits:{Analytical_Thinking:15, Communication:10}},
    ]},
  ],

  pg: [
    { q:"Your research supervisor rejects your entire thesis chapter. You:", options:[
      {label:"Seek a detailed review meeting to understand the exact issues", traits:{Communication:15, Analytical_Thinking:10}},
      {label:"Reflect independently, then come back with a revised framework", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Seek feedback from peers or another faculty for second opinion", traits:{Teamwork:10, Decision_Making:10}},
      {label:"Accept it, take a break, and return with fresh perspective", traits:{Adaptability:15, Confidence:10}},
    ]},
    { q:"You find a significant gap in existing literature. You:", options:[
      {label:"Design a study specifically to address that gap", traits:{Curiosity:15, Decision_Making:10}},
      {label:"Extend your current research to cover the gap", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Publish a theoretical paper proposing how it could be addressed", traits:{Creativity:15, Communication:10}},
      {label:"Collaborate with others to jointly investigate the gap", traits:{Teamwork:15, Leadership:10}},
    ]},
    { q:"A journal rejects your paper citing insufficient methodological rigor. You:", options:[
      {label:"Analyse the reviewers comments carefully and revise systematically", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Submit to a different journal with lower standards", traits:{Decision_Making:10, Adaptability:10}},
      {label:"Strengthen the methodology section and resubmit to same journal", traits:{Persistence:15, Confidence:10}},
      {label:"Consult a statistician or methodologist for expert input", traits:{Communication:15, Teamwork:10}},
    ]},
    { q:"You present research to both academic peers and industry professionals. You:", options:[
      {label:"Prepare two versions: one technical, one application-focused", traits:{Communication:15, Analytical_Thinking:10}},
      {label:"Lead with the problem it solves, then go into methodology", traits:{Leadership:15, Communication:10}},
      {label:"Use heavy data visualization to bridge both audiences", traits:{Creativity:15, Analytical_Thinking:10}},
      {label:"Prepare ready Q&A knowing what each group will ask", traits:{Decision_Making:15, Persistence:10}},
    ]},
    { q:"Halfway through your research, a new study contradicts your hypothesis. You:", options:[
      {label:"Reassess my hypothesis and adjust the research design", traits:{Adaptability:15, Analytical_Thinking:10}},
      {label:"Analyse differences in methodology between the two studies", traits:{Analytical_Thinking:15, Curiosity:10}},
      {label:"Continue and clearly discuss the contradiction in findings", traits:{Confidence:15, Persistence:10}},
      {label:"Seek supervisor guidance on whether to pivot or continue", traits:{Communication:10, Decision_Making:15}},
    ]},
    { q:"You are asked to teach a graduate seminar on your specialization. You:", options:[
      {label:"Design it around the cutting-edge questions in the field", traits:{Curiosity:15, Leadership:10}},
      {label:"Structure it to build foundational knowledge before advanced topics", traits:{Communication:15, Analytical_Thinking:10}},
      {label:"Make it highly interactive with student-led discussions", traits:{Teamwork:15, Communication:10}},
      {label:"Focus on real-world applications of the theory", traits:{Creativity:15, Decision_Making:10}},
    ]},
  ],

  professional: [
    { q:"A client requests a course of action you know is professionally inadvisable. You:", options:[
      {label:"Explain the risks clearly and document your advice in writing", traits:{Communication:15, Decision_Making:10}},
      {label:"Refuse to proceed and refer them to a colleague", traits:{Confidence:15, Decision_Making:10}},
      {label:"Present alternative approaches that achieve their goal responsibly", traits:{Analytical_Thinking:15, Communication:10}},
      {label:"Proceed under protest with full risk disclosure documented", traits:{Adaptability:10, Confidence:10}},
    ]},
    { q:"A significant systemic error is discovered in your department. You are senior. You:", options:[
      {label:"Own the problem publicly, lead the investigation and fix it", traits:{Leadership:15, Confidence:10}},
      {label:"Convene a rapid response team to diagnose and contain the issue", traits:{Decision_Making:15, Teamwork:10}},
      {label:"Communicate transparently with all stakeholders about status", traits:{Communication:15, Leadership:10}},
      {label:"Analyse root cause first before making any public statement", traits:{Analytical_Thinking:15, Decision_Making:10}},
    ]},
    { q:"Two senior colleagues hold opposing views on a critical decision. You:", options:[
      {label:"Present evidence-based analysis supporting one view clearly", traits:{Analytical_Thinking:15, Confidence:10}},
      {label:"Facilitate a structured discussion to find consensus", traits:{Leadership:15, Communication:10}},
      {label:"Propose a pilot approach that tests both views at small scale", traits:{Decision_Making:15, Creativity:10}},
      {label:"Escalate to senior leadership for a final decision", traits:{Communication:10, Adaptability:10}},
    ]},
    { q:"Approached with a project with significant reward but ethical ambiguity. You:", options:[
      {label:"Decline if ethical concerns cannot be fully resolved", traits:{Decision_Making:15, Confidence:10}},
      {label:"Seek independent ethical or legal counsel before deciding", traits:{Analytical_Thinking:15, Decision_Making:10}},
      {label:"Take the project but put in place strong safeguards and oversight", traits:{Leadership:15, Adaptability:10}},
      {label:"Discuss with colleagues or professional body for guidance", traits:{Communication:15, Teamwork:10}},
    ]},
    { q:"Asked to mentor a junior professional who is underperforming. You:", options:[
      {label:"Have a direct conversation about specific gaps and set clear targets", traits:{Communication:15, Leadership:10}},
      {label:"Observe their work closely to understand root cause first", traits:{Analytical_Thinking:15, Persistence:10}},
      {label:"Provide extra training resources and coaching proactively", traits:{Leadership:15, Communication:10}},
      {label:"Involve HR or a formal review process to structure improvement", traits:{Decision_Making:15, Communication:10}},
    ]},
    { q:"You disagree strongly with a new institutional policy. You:", options:[
      {label:"Voice opposition through formal channels with evidence-based arguments", traits:{Communication:15, Confidence:10}},
      {label:"Comply while working internally to change it through legitimate channels", traits:{Adaptability:15, Persistence:10}},
      {label:"Engage peers to build consensus around an alternative proposal", traits:{Leadership:15, Teamwork:10}},
      {label:"Seek senior leadership view before forming a firm position", traits:{Analytical_Thinking:10, Communication:10}},
    ]},
  ]
};

/* -- CAREER INTEREST BANK ------------------------------------- */
const INTEREST_BANK = [
  { q:"Which activity sounds more engaging?",
    a:{label:"Building AI systems and robots", domains:{Technology:2, Engineering:1}},
    b:{label:"Creating business strategies", domains:{Business:2}} },
  { q:"Which sounds more fulfilling?",
    a:{label:"Teaching and mentoring students", domains:{Education:2, Social_Service:1}},
    b:{label:"Diagnosing and treating patients", domains:{Healthcare:2, Social_Service:1}} },
  { q:"Which problem excites you most?",
    a:{label:"Solving complex algorithms", domains:{Technology:2, Research:1}},
    b:{label:"Designing creative campaigns", domains:{Arts_Creative:2, Business:1}} },
  { q:"Where would you prefer to work?",
    a:{label:"Research laboratory or technology company", domains:{Research:2, Technology:1}},
    b:{label:"Courtroom or law firm", domains:{Law:2}} },
  { q:"Which career path interests you?",
    a:{label:"Engineering large-scale infrastructure", domains:{Engineering:2}},
    b:{label:"Working in environmental conservation", domains:{Environment:2, Social_Service:1}} },
  { q:"Which project would you prefer?",
    a:{label:"Building a data analytics platform", domains:{Technology:2, Research:1}},
    b:{label:"Launching a social enterprise", domains:{Business:1, Social_Service:2}} },
  { q:"Which role suits you better?",
    a:{label:"Medical researcher developing vaccines", domains:{Healthcare:2, Research:1}},
    b:{label:"Journalist writing investigative reports", domains:{Research:1, Social_Service:1, Arts_Creative:1}} },
  { q:"What would you enjoy more?",
    a:{label:"Designing a new sustainable city", domains:{Engineering:2, Environment:1}},
    b:{label:"Teaching rural communities new skills", domains:{Education:2, Social_Service:1}} },
  { q:"Which work environment appeals to you?",
    a:{label:"Hospital or medical clinic helping patients", domains:{Healthcare:2, Social_Service:1}},
    b:{label:"Startup company building innovative products", domains:{Technology:2, Business:1}} },
  { q:"Which would be more satisfying to achieve?",
    a:{label:"Developing a life-saving medical device", domains:{Healthcare:2, Engineering:1}},
    b:{label:"Winning a major legal case for justice", domains:{Law:2, Social_Service:1}} },
  { q:"Which skill set appeals to you more?",
    a:{label:"Data analysis and statistical research", domains:{Research:2, Technology:1}},
    b:{label:"Public speaking and persuasion", domains:{Business:1, Education:1, Law:1}} },
  { q:"Which challenge would you rather tackle?",
    a:{label:"Reducing carbon emissions through technology", domains:{Environment:2, Engineering:1}},
    b:{label:"Creating a bestselling app or game", domains:{Technology:2, Arts_Creative:1}} },
  { q:"How would you most like to serve others?",
    a:{label:"Providing mental health support and counselling", domains:{Healthcare:2, Social_Service:1}},
    b:{label:"Building infrastructure in underserved areas", domains:{Engineering:2, Social_Service:1}} },
  { q:"Which type of creative work interests you?",
    a:{label:"Designing user interfaces and digital experiences", domains:{Arts_Creative:2, Technology:1}},
    b:{label:"Writing books, scripts or content", domains:{Arts_Creative:2, Education:1}} },
  { q:"Which professional identity appeals to you more?",
    a:{label:"A scientist publishing research on climate change", domains:{Research:2, Environment:1}},
    b:{label:"A lawyer fighting for human rights", domains:{Law:2, Social_Service:1}} },
  { q:"What kind of impact do you want to create?",
    a:{label:"Educating the next generation of professionals", domains:{Education:2, Social_Service:1}},
    b:{label:"Building businesses that create jobs and wealth", domains:{Business:2}} },
  { q:"Which kind of work day sounds better?",
    a:{label:"Designing mechanical or electrical systems", domains:{Engineering:2}},
    b:{label:"Managing finances and investment strategies", domains:{Business:2}} },
  { q:"Which challenge interests you most?",
    a:{label:"Developing a cure for a rare disease", domains:{Healthcare:2, Research:1}},
    b:{label:"Reducing inequality through social programs", domains:{Social_Service:2, Education:1}} },
  { q:"Which project would you choose to lead?",
    a:{label:"A national biodiversity conservation program", domains:{Environment:2, Research:1}},
    b:{label:"An AI-powered product for education", domains:{Technology:2, Education:1}} },
  { q:"If you wrote a book, what would it be about?",
    a:{label:"Scientific discoveries changing the world", domains:{Research:2, Technology:1}},
    b:{label:"Stories of justice, law and society", domains:{Law:2, Social_Service:1}} },
  { q:"What gives you the deepest sense of meaning?",
    a:{label:"Creating something beautiful that moves people emotionally", domains:{Arts_Creative:2}},
    b:{label:"Solving complex structural or mechanical problems", domains:{Engineering:2}} },
  { q:"Which career milestone excites you most?",
    a:{label:"Publishing a research paper in a top journal", domains:{Research:2}},
    b:{label:"Starting and successfully running my own company", domains:{Business:2}} },
  { q:"Which situation would you find most rewarding?",
    a:{label:"Successfully diagnosing and treating a difficult patient", domains:{Healthcare:2}},
    b:{label:"Leading a team that delivers a breakthrough technology", domains:{Technology:2, Engineering:1}} },
  { q:"Which area of study inspires you most?",
    a:{label:"Biology, medicine and the human body", domains:{Healthcare:2, Research:1}},
    b:{label:"Physics, maths and engineering design", domains:{Engineering:2, Research:1}} },
  { q:"How do you prefer to help solve societal problems?",
    a:{label:"Through community education and empowerment programs", domains:{Education:2, Social_Service:1}},
    b:{label:"Through technology and innovation", domains:{Technology:2, Engineering:1}} },
  { q:"Which type of innovation excites you?",
    a:{label:"Biomedical innovation - new drugs, devices, treatments", domains:{Healthcare:2, Engineering:1}},
    b:{label:"Sustainable technology - clean energy, green design", domains:{Environment:2, Engineering:1}} },
  { q:"Which knowledge gives you the most satisfaction?",
    a:{label:"Understanding why diseases happen at a molecular level", domains:{Research:2, Healthcare:1}},
    b:{label:"Understanding how economies and markets function", domains:{Business:2, Research:1}} },
  { q:"Which role would make you most proud?",
    a:{label:"A judge making fair and wise decisions", domains:{Law:2}},
    b:{label:"A professor shaping the minds of future professionals", domains:{Education:2, Research:1}} },
  { q:"Which project would you find most fulfilling?",
    a:{label:"Designing a city park system that reduces pollution", domains:{Environment:2, Engineering:1}},
    b:{label:"Creating an animation series that tells important stories", domains:{Arts_Creative:2, Social_Service:1}} },
  { q:"Which experience would you prefer?",
    a:{label:"Leading a medical mission in a remote community", domains:{Healthcare:2, Social_Service:1}},
    b:{label:"Architecting a scalable cloud system used by millions", domains:{Technology:2, Engineering:1}} },
];

/* -- CAREER SKILL MAP (30 Careers) ----------------------------- */
const CAREER_SKILL_MAP = {
  "Psychologist":              ["Communication","Empathy","Observation","Analytical Thinking","Research","Active Listening","Report Writing"],
  "Software Developer":        ["Programming","Logical Thinking","Problem Solving","Debugging","Analytical Thinking","Computer Skills","Version Control"],
  "Data Scientist":            ["Statistics","Mathematics","Programming","Data Analysis","Machine Learning","Analytical Thinking","Data Visualization"],
  "Full Stack Developer":      ["Programming","Web Development","Frontend Skills","Backend Skills","Database Management","Problem Solving","API Design"],
  "Doctor":                    ["Biology","Medical Knowledge","Communication","Decision Making","Problem Solving","Empathy","Clinical Skills"],
  "Data Analyst":              ["Data Analysis","Statistics","Excel / BI Tools","SQL & Databases","Data Visualization","Critical Thinking","Reporting"],
  "Machine Learning Engineer": ["Machine Learning","Programming","Mathematics","Data Analysis","Deep Learning","Model Deployment","Research"],
  "AI Engineer":               ["Artificial Intelligence","Machine Learning","Programming","Mathematics","Problem Solving","Research","System Design"],
  "Entrepreneur":              ["Business Planning","Leadership","Decision Making","Communication","Financial Literacy","Creativity","Risk Management"],
  "School Teacher":            ["Communication","Teaching","Patience","Subject Knowledge","Creativity","Empathy","Classroom Management"],
  "Business Analyst":          ["Analytical Thinking","Communication","Problem Solving","Business Knowledge","Data Analysis","Requirements Gathering","Process Mapping"],
  "Professor / Researcher":    ["Research","Academic Writing","Subject Expertise","Analytical Thinking","Communication","Teaching","Critical Thinking"],
  "Lawyer":                    ["Communication","Logical Reasoning","Critical Thinking","Research","Argumentation","Decision Making","Legal Writing"],
  "Cyber Security Analyst":    ["Networking","Security Protocols","Ethical Hacking","Analytical Thinking","Programming","Risk Assessment","Incident Response"],
  "Chartered Accountant":      ["Financial Accounting","Taxation","Auditing","Analytical Thinking","Attention to Detail","Regulatory Knowledge","Tally / ERP"],
  "Product Manager":           ["Product Strategy","Communication","Data Analysis","Leadership","User Research","Decision Making","Market Analysis"],
  "Cloud Architect":           ["Cloud Computing","System Design","Networking","Security","Programming","Infrastructure Planning","Cost Optimization"],
  "Bank Manager":              ["Financial Knowledge","Communication","Leadership","Decision Making","Customer Service","Risk Assessment","Team Management"],
  "Mechanical Engineer":       ["Mechanical Design","CAD & Drafting","Thermodynamics","Mathematics","Problem Solving","Materials Science","Manufacturing"],
  "Civil Engineer":            ["Structural Analysis","CAD & Drafting","Mathematics","Project Management","Material Science","Surveying","Construction Knowledge"],
  "UI/UX Designer":            ["Creativity","User Research","Design Tools","Visual Thinking","Communication","Problem Solving","Prototyping"],
  "Graphic Designer":          ["Creativity","Design Tools","Visual Thinking","Typography","Color Theory","Communication","Brand Identity"],
  "Nurse":                     ["Patient Care","Communication","Empathy","Medical Knowledge","Decision Making","Attention to Detail","Teamwork"],
  "Pharmacist":                ["Pharmacology","Chemistry","Communication","Attention to Detail","Patient Counseling","Medical Knowledge","Analytical Thinking"],
  "Architect":                 ["Architectural Design","CAD & Drafting","Creativity","Structural Knowledge","Project Management","Communication","Spatial Thinking"],
  "Electrical Engineer":       ["Circuit Design","Electrical Systems","Mathematics","Problem Solving","CAD & Drafting","Programming","Safety Standards"],
  "Agricultural Scientist":    ["Biology","Agricultural Science","Research","Data Analysis","Field Work","Environmental Knowledge","Problem Solving"],
  "Biomedical Engineer":       ["Biology","Engineering Principles","Research","Medical Devices","Problem Solving","Mathematics","Programming"],
  "Animator":                  ["Animation Tools","Creativity","Visual Storytelling","Drawing","Attention to Detail","3D Modeling","Teamwork"],
  "Environmental Scientist":   ["Environmental Science","Research","Data Analysis","Chemistry","Field Work","Report Writing","Environmental Policy"],
};



/* -- SKILL QUIZ BANK ------------------------------------------ */
const SKILL_QUIZ_BANK = {
  "Programming": [
    { q:"Which data type stores True/False in most languages?", opts:["Integer","Boolean","String","Float"], ans:1 },
    { q:"What does a loop do?", opts:["Declares a variable","Repeats code until a condition is met","Defines a function","Stores data"], ans:1 },
    { q:"Output of print(2**3) in Python?", opts:["6","8","9","5"], ans:1 },
  ],
  "Statistics": [
    { q:"Median of 3,5,7,9,11?", opts:["5","7","9","6"], ans:1 },
    { q:"Standard deviation measures?", opts:["Average","Spread of data","Skewness","Frequency"], ans:1 },
    { q:"Correlation coefficient of 1 means?", opts:["No correlation","Perfect negative","Perfect positive","Weak correlation"], ans:2 },
  ],
  "Machine Learning": [
    { q:"Supervised learning uses?", opts:["Unlabeled data","Reinforcement signals","Labeled training data","Transfer models"], ans:2 },
    { q:"Algorithm for classification tasks?", opts:["K-Means","Linear Regression","Logistic Regression","PCA"], ans:2 },
    { q:"Overfitting means the model?", opts:["Performs well on test data","Is too simple","Memorizes training data and fails on new data","Is not trained enough"], ans:2 },
  ],
  "Data Analysis": [
    { q:"VLOOKUP in Excel is used to?", opts:["Create charts","Search for a value in a column and return a result","Sort data","Filter rows"], ans:1 },
    { q:"Pivot Table is used to?", opts:["Write macros","Summarize and analyze large data sets","Create graphs","Protect sheets"], ans:1 },
    { q:"Best chart type for trends over time?", opts:["Pie chart","Bar chart","Line chart","Scatter plot"], ans:2 },
  ],
  "Communication": [
    { q:"Most important element of effective communication?", opts:["Talking fast","Being understood by the listener","Using difficult words","Speaking formally"], ans:1 },
    { q:"Active listening means?", opts:["Waiting for your turn to talk","Fully concentrating and understanding the speaker","Looking at your phone","Planning what to say next"], ans:1 },
    { q:"Non-verbal communication is?", opts:["Written messages","Body language, gestures and facial expressions","Phone calls","Emails"], ans:1 },
  ],
  "SQL & Databases": [
    { q:"SQL command to retrieve data from a table?", opts:["INSERT","UPDATE","SELECT","DELETE"], ans:2 },
    { q:"GROUP BY in SQL does what?", opts:["Sorts rows","Filters rows","Groups rows by column values","Joins tables"], ans:2 },
    { q:"Primary key uniquely identifies?", opts:["Foreign Key","Unique Key","Each row in a table","Index Key"], ans:2 },
  ],
  "Analytical Thinking": [
    { q:"Logical deduction: If A > B and B > C, then?", opts:["B > A","A > C","C > A","Cannot determine"], ans:1 },
    { q:"Best approach to solve a complex problem?", opts:["Guess randomly","Break into smaller sub-problems","Ask someone else","Ignore sub-problems"], ans:1 },
    { q:"Critical thinking requires?", opts:["Accepting information at face value","Questioning assumptions and evaluating evidence","Following majority opinion","Memorising facts"], ans:1 },
  ],
  "Empathy": [
    { q:"Empathy means?", opts:["Feeling superior to others","Understanding and sharing the feelings of another person","Giving advice quickly","Solving others' problems for them"], ans:1 },
    { q:"When a colleague is stressed, the best empathetic response is?", opts:["Tell them to calm down","Listen without interrupting and acknowledge their feelings","Immediately give solutions","Change the subject"], ans:1 },
    { q:"Empathy in professional settings helps in?", opts:["Winning arguments","Building stronger relationships and trust","Being more authoritative","Avoiding difficult conversations"], ans:1 },
  ],
  "Creativity": [
    { q:"Brainstorming is used for?", opts:["Evaluating existing ideas","Generating many new ideas freely","Eliminating ideas","Analysing budgets"], ans:1 },
    { q:"Which mindset supports creativity most?", opts:["Fixed mindset","Growth mindset","Risk-averse mindset","Perfectionist mindset"], ans:1 },
    { q:"Design thinking starts with?", opts:["Prototyping","Empathizing with users","Launching the product","Defining metrics"], ans:1 },
  ],
  "Research": [
    { q:"A literature review is done to?", opts:["Present your findings","Survey existing knowledge on a topic","Collect primary data","Summarize your conclusion"], ans:1 },
    { q:"Primary data is collected by?", opts:["Reading published papers","Conducting surveys, interviews or experiments","Using existing databases","Searching the internet"], ans:1 },
    { q:"Peer review in research ensures?", opts:["Faster publication","Quality and credibility of research","More citations","Wider distribution"], ans:1 },
  ],
  "Financial Accounting": [
    { q:"Balance Sheet shows?", opts:["Profit and Loss","Cash flows","Assets, liabilities and equity at a point in time","Revenue and expenses"], ans:2 },
    { q:"Depreciation is?", opts:["Increase in asset value","Allocation of asset cost over useful life","Cash payment for assets","Tax deduction"], ans:1 },
    { q:"Accrual basis records revenue when?", opts:["Cash received","Revenue earned","Month end","Invoice sent"], ans:1 },
  ],
  "Leadership": [
    { q:"Good leader in a crisis should first?", opts:["Blame others","Stay calm and assess the situation","Ignore the problem","Make decisions without consulting anyone"], ans:1 },
    { q:"Delegation means?", opts:["Doing all the work yourself","Assigning tasks to team members based on strengths","Avoiding responsibility","Micromanaging every task"], ans:1 },
    { q:"Transformational leadership focuses on?", opts:["Maintaining status quo","Inspiring followers to achieve beyond expectations","Only rewarding performance","Strict hierarchical control"], ans:1 },
  ],
  "Medical Knowledge": [
    { q:"Which organ filters blood and produces urine?", opts:["Liver","Heart","Kidney","Lung"], ans:2 },
    { q:"Normal human body temperature?", opts:["35°C","37°C","39°C","33°C"], ans:1 },
    { q:"ECG/EKG measures?", opts:["Brain activity","Heart electrical activity","Blood pressure","Oxygen levels"], ans:1 },
  ],
  "Biology": [
    { q:"DNA is found primarily in?", opts:["Cell membrane","Cytoplasm","Nucleus","Ribosome"], ans:2 },
    { q:"Photosynthesis converts?", opts:["Oxygen to CO2","CO2 and water to glucose using sunlight","Glucose to oxygen","Water to energy"], ans:1 },
    { q:"Powerhouse of the cell?", opts:["Nucleus","Ribosome","Mitochondria","Endoplasmic reticulum"], ans:2 },
  ],
  "Problem Solving": [
    { q:"First step in structured problem solving?", opts:["Implementing a solution","Evaluating results","Clearly defining the problem","Generating alternatives"], ans:2 },
    { q:"Root cause analysis is used to?", opts:["Find symptoms","Find the underlying reason for a problem","Document incidents","Allocate blame"], ans:1 },
    { q:"Decision tree is useful for?", opts:["Database design","Visualizing choices and their consequences","Drawing flowcharts","Writing algorithms only"], ans:1 },
  ],
  "Networking": [
    { q:"IP stands for?", opts:["Interface Protocol","Internet Protocol","Internal Processing","Interconnected Ports"], ans:1 },
    { q:"Firewall is used to?", opts:["Speed up the internet","Monitor and control incoming/outgoing network traffic","Store data","Connect WiFi"], ans:1 },
    { q:"VPN stands for?", opts:["Virtual Packet Network","Very Private Node","Virtual Private Network","Verified Protocol Network"], ans:2 },
  ],
  "Mathematics": [
    { q:"Derivative of sin(x)?", opts:["cos(x)","-cos(x)","sin(x)","-sin(x)"], ans:0 },
    { q:"Determinant of [[a,b],[c,d]]?", opts:["ab+cd","ac-bd","ad-bc","ad+bc"], ans:2 },
    { q:"Integral of 2x dx?", opts:["x²+C","2x²+C","x+C","2+C"], ans:0 },
  ],
  "Environmental Science": [
    { q:"Greenhouse effect is caused by?", opts:["Ozone layer","Atmospheric gases trapping heat","Ocean currents","Deforestation only"], ans:1 },
    { q:"Biodiversity hotspot means?", opts:["Hottest place on Earth","Area with high species diversity under threat","Tourist destination","Volcanic region"], ans:1 },
    { q:"Primary contributor to global warming?", opts:["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"], ans:2 },
  ],
  "CAD & Drafting": [
    { q:"CAD stands for?", opts:["Computer Aided Drafting","Computer Aided Design","Computer Application Drawing","Computerized Assembly Design"], ans:1 },
    { q:"Widely used software for 3D mechanical design?", opts:["Photoshop","SolidWorks / AutoCAD","Excel","MATLAB"], ans:1 },
    { q:"Orthographic projection shows?", opts:["A 3D perspective view","Multiple 2D views of a 3D object","Only the front view","A cross-section"], ans:1 },
  ],
  "UI/UX Design": [
    { q:"A wireframe in UI/UX is?", opts:["A color palette","A low-fidelity visual layout of an interface","A finished product design","A coding framework"], ans:1 },
    { q:"Which principle states similar elements should look similar?", opts:["Contrast","Proximity","Consistency","Alignment"], ans:2 },
    { q:"User testing is done to?", opts:["Debug code","Evaluate if users can use the product as intended","Train designers","Measure developer speed"], ans:1 },
  ],
  // ── Additional skill quizzes ──────────────────────────────────────────
  "Chemistry": [
    { q:"Atomic number of Carbon?", opts:["6","8","12","14"], ans:0 },
    { q:"pH of pure water at 25°C?", opts:["6","7","8","9"], ans:1 },
    { q:"Avogadro's number is approximately?", opts:["6.022×10²³","3.0×10⁸","1.6×10⁻¹⁹","9.8"], ans:0 },
  ],
  "Deep Learning": [
    { q:"A neural network's 'activation function' does what?", opts:["Stores weights","Introduces non-linearity to the output","Normalizes input data","Reduces overfitting"], ans:1 },
    { q:"CNN is mainly used for?", opts:["Text classification","Time series analysis","Image recognition","Reinforcement learning"], ans:2 },
    { q:"Backpropagation is used to?", opts:["Feed data forward","Update weights using gradients","Increase layers","Select activation functions"], ans:1 },
  ],
  "Web Development": [
    { q:"HTML is used for?", opts:["Styling pages","Adding interactivity","Structuring content","Database queries"], ans:2 },
    { q:"Which language makes web pages interactive?", opts:["HTML","CSS","JavaScript","SQL"], ans:2 },
    { q:"REST API returns data in which format?", opts:["HTML","XML only","JSON","CSV"], ans:2 },
  ],
  "Frontend Skills": [
    { q:"CSS Flexbox is used to?", opts:["Animate elements","Lay out elements in one dimension","Create 3D effects","Connect to APIs"], ans:1 },
    { q:"React is a?", opts:["Database","Backend framework","JavaScript UI library","CSS framework"], ans:2 },
    { q:"What does 'responsive design' mean?", opts:["Fast loading","Layout adapts to different screen sizes","Dark mode support","Offline capability"], ans:1 },
  ],
  "Backend Skills": [
    { q:"REST stands for?", opts:["Remote Execution Standard Transfer","Representational State Transfer","Rapid Event Sending Technology","Request-Event Server Type"], ans:1 },
    { q:"Which is a backend language?", opts:["HTML","CSS","Node.js / Python","Figma"], ans:2 },
    { q:"Middleware in backend development?", opts:["A type of database","Software that connects components or services","A UI library","A testing tool"], ans:1 },
  ],
  "Data Visualization": [
    { q:"Which chart compares categories?", opts:["Line chart","Bar chart","Scatter plot","Histogram"], ans:1 },
    { q:"Tableau is used for?", opts:["Writing code","Business intelligence and visual analytics","Database management","Network monitoring"], ans:1 },
    { q:"A heatmap shows?", opts:["Geographic locations","Magnitude of values using color intensity","Process flow","Relationship between two variables"], ans:1 },
  ],
  "Database Management": [
    { q:"RDBMS stands for?", opts:["Relational Database Management System","Remote Data Backup Management System","Rapid Database Migration System","None of the above"], ans:0 },
    { q:"What is normalization in databases?", opts:["Speeding up queries","Organizing data to reduce redundancy","Backing up data","Encrypting data"], ans:1 },
    { q:"Which command removes all rows from a table without deleting it?", opts:["DROP","DELETE","TRUNCATE","REMOVE"], ans:2 },
  ],
  "Cloud Computing": [
    { q:"IaaS stands for?", opts:["Internet as a Service","Infrastructure as a Service","Integration as a Service","Intelligence as a Service"], ans:1 },
    { q:"Which is a cloud provider?", opts:["Oracle DB","Amazon Web Services (AWS)","Linux","Apache"], ans:1 },
    { q:"Scalability in cloud means?", opts:["Paying less money","Ability to handle increased load by adding resources","Faster internet","Automatic code deployment"], ans:1 },
  ],
  "System Design": [
    { q:"Load balancer is used to?", opts:["Store data","Distribute incoming requests across multiple servers","Encrypt traffic","Monitor CPU usage"], ans:1 },
    { q:"CAP theorem relates to?", opts:["Network security","Consistency, Availability, and Partition tolerance","CPU, Architecture, and Performance","Caching strategies"], ans:1 },
    { q:"Microservices architecture means?", opts:["One large application","Application split into small independent services","A UI pattern","Shared database approach"], ans:1 },
  ],
  "Logical Reasoning": [
    { q:"All men are mortal. Socrates is a man. Therefore?", opts:["Socrates is immortal","Socrates is mortal","Some men are mortal","Cannot determine"], ans:1 },
    { q:"Next in series: 2, 6, 12, 20, ?", opts:["28","30","32","36"], ans:1 },
    { q:"Opposite of 'always' is?", opts:["Often","Never","Sometimes","Usually"], ans:1 },
  ],
  "Logical Thinking": [
    { q:"Which is a valid logical argument form?", opts:["If A then B; B is true; so A is true","If A then B; A is true; so B is true","If A then B; B is false; so B is true","None are valid"], ans:1 },
    { q:"Flowcharts are used to?", opts:["Design databases","Represent processes or algorithms step-by-step","Write code","Draw UIs"], ans:1 },
    { q:"An algorithm must be?", opts:["Creative","Finite and unambiguous","Written in Python","Object-oriented"], ans:1 },
  ],
  "Decision Making": [
    { q:"A decision matrix helps to?", opts:["Write code","Evaluate multiple options against criteria","Debug software","Train employees"], ans:1 },
    { q:"Cognitive bias in decisions means?", opts:["Making rational choices","Systematic errors in thinking affecting judgment","Using data exclusively","Delegating all decisions"], ans:1 },
    { q:"SWOT analysis is used for?", opts:["Security testing","Strategic planning by analyzing strengths, weaknesses, opportunities, threats","Code review","Financial reporting"], ans:1 },
  ],
  "Critical Thinking": [
    { q:"Which is NOT a critical thinking skill?", opts:["Inference","Memorization","Evaluation","Analysis"], ans:1 },
    { q:"Confirmation bias means?", opts:["Seeking evidence that contradicts your view","Favouring information that confirms existing beliefs","Making quick decisions","Over-analysing data"], ans:1 },
    { q:"Socratic questioning is used to?", opts:["Memorize facts","Stimulate critical thinking through probing questions","Speed up decision making","Organize information"], ans:1 },
  ],
  "Structural Analysis": [
    { q:"Bending moment in a beam is caused by?", opts:["Torsion","Transverse loads creating internal moments","Axial compression only","Temperature changes"], ans:1 },
    { q:"A cantilever beam is fixed at?", opts:["Both ends","One end only","The middle","No end"], ans:1 },
    { q:"Factor of safety is used to?", opts:["Increase cost","Provide a margin against failure","Reduce material use","Speed up construction"], ans:1 },
  ],
  "Circuit Design": [
    { q:"Ohm's Law states V = ?", opts:["I/R","I×R","R/I","I²×R"], ans:1 },
    { q:"A capacitor stores energy in?", opts:["Magnetic field","Electric field","Heat","Sound"], ans:1 },
    { q:"Semiconductor is?", opts:["Perfect conductor","Perfect insulator","Material with conductivity between conductor and insulator","Magnetic material"], ans:2 },
  ],
  "Mechanical Design": [
    { q:"Stress is defined as?", opts:["Force × Area","Force / Area","Area / Force","Mass × Acceleration"], ans:1 },
    { q:"Gear ratio is used to?", opts:["Measure speed","Change torque and rotational speed between shafts","Measure pressure","Calculate area"], ans:1 },
    { q:"Material property 'ductility' means?", opts:["Hardness","Ability to be drawn into wire without breaking","Resistance to heat","Brittleness"], ans:1 },
  ],
  "Thermodynamics": [
    { q:"First law of thermodynamics states?", opts:["Energy can be destroyed","Energy is conserved — it can only be converted","Heat flows from cold to hot","Entropy always decreases"], ans:1 },
    { q:"Entropy in thermodynamics measures?", opts:["Temperature","Pressure","Disorder or randomness of a system","Volume"], ans:2 },
    { q:"Carnot efficiency depends on?", opts:["Working fluid","Temperature difference between hot and cold reservoirs","Machine size","Material of pistons"], ans:1 },
  ],
  "Electrical Systems": [
    { q:"AC stands for?", opts:["Analog Current","Alternating Current","Amplified Current","Applied Current"], ans:1 },
    { q:"Transformer is used to?", opts:["Convert AC to DC","Change voltage levels in AC circuits","Store electrical energy","Generate electricity"], ans:1 },
    { q:"Power factor in an AC circuit measures?", opts:["Voltage level","Efficiency of power usage (ratio of real to apparent power)","Current frequency","Resistance"], ans:1 },
  ],
  "Pharmacology": [
    { q:"Pharmacokinetics studies?", opts:["Drug effects on body","How the body absorbs, distributes, metabolizes, and excretes drugs","Drug synthesis","Patient counseling"], ans:1 },
    { q:"Analgesics are drugs used for?", opts:["Treating infections","Pain relief","Blood pressure control","Diabetes management"], ans:1 },
    { q:"Half-life of a drug is?", opts:["Time for drug to start working","Time taken for drug concentration to reduce by 50%","Duration of side effects","Time to reach maximum concentration"], ans:1 },
  ],
  "Agricultural Science": [
    { q:"Photosynthesis in crops primarily depends on?", opts:["Soil type","Sunlight, CO2, and water","Rainfall only","Fertilizer type"], ans:1 },
    { q:"NPK fertilizer provides?", opts:["Sodium, Phosphorus, Potassium","Nitrogen, Phosphorus, Potassium","Nitrogen, Protein, Calcium","None of the above"], ans:1 },
    { q:"Drip irrigation is used to?", opts:["Flood fields completely","Deliver water directly to plant roots efficiently","Spray water over large areas","Increase rainfall"], ans:1 },
  ],
  "Project Management": [
    { q:"A Gantt chart shows?", opts:["Budget allocation","Task timeline and dependencies","Team hierarchy","Risk matrix"], ans:1 },
    { q:"Agile methodology is best described as?", opts:["Long sequential phases","Iterative and flexible development with frequent reviews","No planning at all","Only for software projects"], ans:1 },
    { q:"Critical path in a project is?", opts:["Most expensive task","Longest sequence of tasks that determines project duration","Most important task","First task in the plan"], ans:1 },
  ],
  "Market Analysis": [
    { q:"Market segmentation is?", opts:["Analyzing competitors","Dividing a market into distinct groups of buyers","Setting product prices","Creating advertisements"], ans:1 },
    { q:"PEST analysis examines?", opts:["People, Events, Strategies, Technology","Political, Economic, Social, Technological factors","Product, Entry, Sales, Trade","None of the above"], ans:1 },
    { q:"Market share is?", opts:["Total revenue of a company","Percentage of total sales in a market held by a company","Number of customers","Product profit margin"], ans:1 },
  ],
  "Risk Assessment": [
    { q:"Risk is best defined as?", opts:["A certain loss","Probability of an event multiplied by its impact","A past incident","A budget overrun"], ans:1 },
    { q:"A risk register contains?", opts:["Financial reports","Identified risks, their likelihood, impact and mitigation plans","Project timelines","Team contact details"], ans:1 },
    { q:"Mitigation in risk management means?", opts:["Ignoring the risk","Taking steps to reduce the probability or impact of a risk","Transferring all risks","Accepting the worst outcome"], ans:1 },
  ],
  "User Research": [
    { q:"A user persona is?", opts:["A real customer profile","A fictional character representing a target user group","A user survey form","A product prototype"], ans:1 },
    { q:"Usability testing evaluates?", opts:["Code quality","How easily users can complete tasks with a product","Server performance","Design aesthetics"], ans:1 },
    { q:"Affinity mapping in UX research is used to?", opts:["Draw wireframes","Organize and categorize qualitative research findings","Write user stories","Conduct A/B tests"], ans:1 },
  ],
  "Attention to Detail": [
    { q:"What value best represents attention to detail?", opts:["Working fast without checking","Carefully reviewing work before submission","Delegating proofreading to others","Ignoring minor errors"], ans:1 },
    { q:"In a legal document, attention to detail is critical because?", opts:["Documents are long","Small errors can have significant legal consequences","Legal writing is complex","Clients pay more"], ans:1 },
    { q:"Quality control primarily relies on?", opts:["Speed","Systematic checking against defined standards","Team size","Technology only"], ans:1 },
  ],
  "Report Writing": [
    { q:"Executive summary in a report is?", opts:["The conclusion section","A brief overview of the report's key points for busy readers","The methodology section","The bibliography"], ans:1 },
    { q:"Which writing style is preferred in formal reports?", opts:["Casual and conversational","Clear, concise, and objective","Flowery and descriptive","First-person narrative"], ans:1 },
    { q:"Data should be presented in reports using?", opts:["Only text paragraphs","Tables, charts, and visuals with proper labels","Bullet points only","Footnotes only"], ans:1 },
  ],
  "Academic Writing": [
    { q:"Citation in academic writing is used to?", opts:["Add word count","Acknowledge sources and support claims","Make the paper longer","Improve grammar"], ans:1 },
    { q:"A thesis statement in an essay?", opts:["Summarizes the conclusion","Presents the main argument of the paper","Lists references","Introduces the topic broadly"], ans:1 },
    { q:"Plagiarism means?", opts:["Writing in passive voice","Using others' work without proper credit","Using too many citations","Writing informally"], ans:1 },
  ],
  "Teaching": [
    { q:"Bloom's Taxonomy is used in education to?", opts:["Assess teacher performance","Classify educational objectives from simple to complex thinking","Design school buildings","Create exam schedules"], ans:1 },
    { q:"Formative assessment is?", opts:["A final exam","Ongoing assessment during learning to provide feedback","A standardized test","A grading system"], ans:1 },
    { q:"Differentiated instruction means?", opts:["Teaching all students the same way","Adapting teaching methods to meet diverse student needs","Only teaching gifted students","Using only textbooks"], ans:1 },
  ],
  "Teamwork": [
    { q:"Most important factor in effective teamwork?", opts:["Everyone having the same skills","Clear communication and shared goals","A strong hierarchy","Avoiding conflicts at all costs"], ans:1 },
    { q:"Conflict in a team should be?", opts:["Ignored always","Addressed constructively to find solutions","Escalated immediately to management","Hidden from everyone"], ans:1 },
    { q:"Free rider problem in a team means?", opts:["Someone who cycles to work","A member who contributes less but benefits equally","A team that moves too fast","A very productive member"], ans:1 },
  ],
  "Ethical Hacking": [
    { q:"What does a penetration tester do?", opts:["Designs websites","Legally tests systems for vulnerabilities before attackers do","Manages databases","Writes application code"], ans:1 },
    { q:"SQL Injection is?", opts:["A database optimization technique","Inserting malicious SQL code into input fields to manipulate databases","A backup strategy","A sorting algorithm"], ans:1 },
    { q:"Social engineering attack uses?", opts:["Malware","Human psychology to trick people into revealing information","Brute force","Packet sniffing"], ans:1 },
  ],
  "Security Protocols": [
    { q:"HTTPS uses which protocol to encrypt data?", opts:["HTTP","TLS/SSL","FTP","SMTP"], ans:1 },
    { q:"Two-factor authentication adds security by?", opts:["Using a complex password","Requiring a second form of verification beyond a password","Encrypting data","Blocking all traffic"], ans:1 },
    { q:"A firewall primarily protects against?", opts:["Hardware failures","Unauthorized network access","Software bugs","Slow internet"], ans:1 },
  ],
  "Model Deployment": [
    { q:"Containerization using Docker is used to?", opts:["Write ML algorithms","Package applications with their dependencies for consistent deployment","Train neural networks","Store datasets"], ans:1 },
    { q:"A REST API endpoint for an ML model receives?", opts:["Trained weights","Input features and returns predictions","Training data","Model metrics"], ans:1 },
    { q:"Model drift means?", opts:["Model moved to a new server","Model performance degrades over time due to changing data patterns","Model was retrained","Model file was corrupted"], ans:1 },
  ],
  "Artificial Intelligence": [
    { q:"Turing Test evaluates?", opts:["Robot speed","Whether a machine can exhibit intelligent behavior indistinguishable from a human","Algorithm complexity","Hardware capability"], ans:1 },
    { q:"NLP stands for?", opts:["Neural Learning Program","Natural Language Processing","Networked Logic Processor","None of the above"], ans:1 },
    { q:"Reinforcement learning learns through?", opts:["Labeled datasets","Trial and error with rewards and penalties","Clustering data","Transfer learning only"], ans:1 },
  ],
};

/* -- ALL_SKILLS: only skills with quizzes ---------------------- */
// Vague/untestable skills (Observation, Patience, Field Work, Process Mapping,
// Reporting, Material Science, Incident Response, etc.) are excluded from the
// skill picker but CAREER_SKILL_MAP still uses them internally for career matching.
const ALL_SKILLS = Object.keys(SKILL_QUIZ_BANK).sort();

/* -- BOARD SUBJECTS MAP --------------------------------------- */

// Kerala State Board (SCERT Kerala) — 10 subjects per class
// CBSE — 5 subjects per class
const BOARD_SUBJECTS = {
  "Class 7": {
    "Kerala State Board": [
      "First Language Part 1 (Malayalam/Tamil/Kannada)",
      "First Language Part 2 (Literature)",
      "Second Language (English)",
      "Third Language (Hindi/Arabic/Sanskrit)",
      "Mathematics",
      "Natural Science",
      "Social Science",
      "Information Technology (IT)",
      "Work Experience",
      "Physical Education & Health"
    ],
    "CBSE": [
      "English (Language & Literature)",
      "Hindi / Third Language",
      "Mathematics",
      "Science",
      "Social Science"
    ],
    "ICSE": [
      "English",
      "Second Language",
      "Mathematics",
      "Science (Physics, Chemistry, Biology)",
      "History & Civics",
      "Geography",
      "Computer Applications",
      "Art / Music / Physical Education"
    ],
    "default": [
      "Language I",
      "Language II (English)",
      "Mathematics",
      "Science",
      "Social Studies"
    ]
  },
  "Class 8": {
    "Kerala State Board": [
      "First Language Part 1 (Malayalam/Tamil/Kannada)",
      "First Language Part 2 (Literature)",
      "Second Language (English)",
      "Third Language (Hindi/Arabic/Sanskrit)",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "Social Science",
      "Information Technology (IT)"
    ],
    "CBSE": [
      "English (Language & Literature)",
      "Hindi / Third Language",
      "Mathematics",
      "Science",
      "Social Science"
    ],
    "ICSE": [
      "English",
      "Second Language",
      "Mathematics",
      "Science (Physics, Chemistry, Biology)",
      "History & Civics",
      "Geography",
      "Computer Applications",
      "Art / Music / Physical Education"
    ],
    "default": [
      "Language I",
      "Language II (English)",
      "Mathematics",
      "Science",
      "Social Studies"
    ]
  },
  "Class 9": {
    "Kerala State Board": [
      "First Language Part 1 (Malayalam/Tamil/Kannada)",
      "First Language Part 2 (Literature)",
      "Second Language (English)",
      "Third Language (Hindi/Arabic/Sanskrit)",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "Social Science I (History & Geography)",
      "Information Technology (IT)"
    ],
    "CBSE": [
      "English (Language & Literature)",
      "Hindi / Third Language",
      "Mathematics",
      "Science",
      "Social Science"
    ],
    "ICSE": [
      "English",
      "Second Language",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "History & Civics",
      "Geography",
      "Computer Applications"
    ],
    "default": [
      "Language I",
      "Language II (English)",
      "Mathematics",
      "Science",
      "Social Studies"
    ]
  },
  "Class 10": {
    "Kerala State Board": [
      "First Language Part 1 (Malayalam/Tamil/Kannada)",
      "First Language Part 2 (Literature)",
      "Second Language (English)",
      "Third Language (Hindi/Arabic/Sanskrit)",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "Social Science I (History & Geography)",
      "Social Science II / Information Technology (IT)"
    ],
    "CBSE": [
      "English (Language & Literature)",
      "Hindi / Third Language",
      "Mathematics",
      "Science",
      "Social Science"
    ],
    "ICSE": [
      "English",
      "Second Language",
      "Mathematics",
      "Physics",
      "Chemistry",
      "Biology",
      "History & Civics",
      "Geography",
      "Computer Applications"
    ],
    "default": [
      "Language I",
      "Language II (English)",
      "Mathematics",
      "Science",
      "Social Studies"
    ]
  },
  "Higher Secondary (11-12)": {
    "Science (PCM)":      ["Physics","Chemistry","Mathematics","Computer Science","English"],
    "Science (PCB)":      ["Physics","Chemistry","Biology","Mathematics","English"],
    "Science (PCMB)":     ["Physics","Chemistry","Mathematics","Biology","English"],
    "Commerce":           ["Accountancy","Business Studies","Economics","Mathematics","English"],
    "Humanities/Arts":    ["History","Geography","Political Science","Economics","English"],
    "Vocational":         ["Vocational Subject","English","General Foundation Course","IT / Computer","Social Studies"],
    "default":            ["Subject 1","Subject 2","Subject 3","Subject 4","English"],
  },
};

/* -- STATE ---------------------------------------------------- */
let currentStep = 1;
const TOTAL_STEPS = 9;
const state = {
  education: {},
  subjectMarks: [],
  aptitudeAnswers: [],
  psychAnswers: [],
  interestScores: {},
  selectedSkills: [],
  certs: [{ name: "", provider: "" }],
  projs: [{ title: "", tech: "" }],
  psychTraits: {},
  _subjects: [],
  _interestAnswers: [],
  skillsWithLevel: [],
};

let aptitudeQuestions = [];
let psychScenarios = [];
let interestPairs = [];
let certCount = 1;
let projCount = 1;
const state_skillProficiency = {};

/* -- NAVIGATION ----------------------------------------------- */
function updateStepUI(direction) {
  direction = direction || "next";
  document.querySelectorAll(".step-section").forEach(function(s, i) {
    var isTarget = (i + 1 === currentStep);
    if (isTarget) {
      s.classList.add("active");
      s.classList.remove("slide-in-right", "slide-in-left");
      void s.offsetWidth;
      s.classList.add(direction === "next" ? "slide-in-right" : "slide-in-left");
    } else {
      s.classList.remove("active", "slide-in-right", "slide-in-left");
    }
  });
  var progress = document.getElementById("main-progress");
  if (progress) progress.style.width = (currentStep / TOTAL_STEPS * 100) + "%";
  renderStepNav();
}

function renderStepNav() {
  var nav = document.getElementById("step-nav");
  if (!nav) return;
  var labels = ["Education","Marks","Aptitude","Psychometric","Interests","Skills","Certs","Projects","Results"];
  var html = "<div class=\"stepper-wrapper\">";
  labels.forEach(function(label, i) {
    var status = i + 1 < currentStep ? "completed" : i + 1 === currentStep ? "active" : "";
    html += "<div class=\"step-item " + status + "\">";
    html += "<div class=\"step-dot\">" + (i + 1 < currentStep ? "checkmark" : i + 1) + "</div>";
    html += "<div class=\"step-label\">" + label + "</div>";
    html += "</div>";
    if (i < labels.length - 1) {
      html += "<div class=\"step-connector " + (i + 1 < currentStep ? "done" : "") + "\"></div>";
    }
  });
  html += "</div>";
  // Fix checkmark symbol
  nav.innerHTML = html.replace(/checkmark/g, "&#10003;");
}

/* -- School-level helper ---------------------------------------- */
// Class 7-12 students have no projects or professional certifications.
// Steps 7 (Certifications) and 8 (Projects) are skipped for them.
function isSchoolLevel() {
  var edu = state.education ? state.education.education_level : "";
  return ["Class 7","Class 8","Class 9","Class 10","Class 11","Class 12"].includes(edu);
}

// Update step 6/7/8 UI labels based on whether student is school-level
function _applySchoolModeUI() {
  var school = isSchoolLevel();
  var isJunior = ["Class 7","Class 8","Class 9","Class 10"].includes(
    state.education ? state.education.education_level : "");

  // Step 6 Next button
  var btn6 = document.getElementById("step6-next-btn");
  if (btn6) btn6.textContent = isJunior
    ? "Get Career Prediction \u2192"
    : (school ? "Next: Achievements \u2192" : "Next: Certifications \u2192");

  if (school) {
    // Step 7: rename to Achievements & Awards
    var t7 = document.getElementById("step7-title");
    var s7 = document.getElementById("step7-subtitle");
    var n7 = document.getElementById("cert-label-name");
    var p7 = document.getElementById("cert-label-provider");
    var ni7 = document.getElementById("cert-name-0");
    var pi7 = document.getElementById("cert-provider-0");
    if (t7) t7.textContent = "Step 7: Achievements & Awards";
    if (s7) s7.textContent = "Add Olympiad medals, school awards, or online course certificates (optional)";
    if (n7) n7.textContent = "Achievement / Award Name";
    if (p7) p7.textContent = "Organiser / Platform";
    if (ni7) ni7.placeholder = "e.g. District Science Olympiad Gold, NTSE Qualifier";
    if (pi7) pi7.placeholder = "e.g. CBSE, State Board, Khan Academy";

    // Step 8: rename to Science Projects & Activities
    var t8 = document.getElementById("step8-title");
    var s8 = document.getElementById("step8-subtitle");
    if (t8) t8.textContent = "Step 8: School Projects & Activities";
    if (s8) s8.textContent = "Add science fair projects, school club activities, or hobbies (optional)";

    // Update proj placeholders
    var pt0 = document.getElementById("proj-title-0");
    var pc0 = document.getElementById("proj-tech-0");
    if (pt0) pt0.placeholder = "e.g. Solar Energy Model, App for Attendance";
    if (pc0) pc0.placeholder = "e.g. Thermocol + Solar Panel / Python / Cardboard";
  }
}

function nextStep(from) {
  if (from === 1) {
    var levelEl = document.getElementById("education_level");
    var boardEl = document.getElementById("board");
    if (!levelEl.value || !boardEl.value) {
      if (!levelEl.value) { levelEl.classList.remove("error-shake"); void levelEl.offsetWidth; levelEl.classList.add("error-shake"); }
      if (!boardEl.value) { boardEl.classList.remove("error-shake"); void boardEl.offsetWidth; boardEl.classList.add("error-shake"); }
      Toast.show("Please select Education Level and Board.", "error");
      return;
    }
    levelEl.classList.remove("error-shake");
    boardEl.classList.remove("error-shake");
    var streamEl = document.getElementById("stream");
    var degreeEl = document.getElementById("degree");
    var specEl = document.getElementById("specialization");
    var instEl = document.getElementById("institution");
    var cgpaEl = document.getElementById("cgpa");
    var attendEl = document.getElementById("attendance");
    state.education = {
      education_level: levelEl.value,
      board: boardEl.value,
      stream: streamEl ? streamEl.value : "",
      degree: degreeEl ? degreeEl.value : "",
      specialization: specEl ? specEl.value : "",
      institution: instEl ? instEl.value : "",
      cgpa: parseFloat(cgpaEl ? cgpaEl.value : 0) || 0,
      attendance: parseFloat(attendEl ? attendEl.value : 0) || 0,
    };
    loadSubjectMarks();
  }
  if (from === 2) saveSubjectMarks();
  if (from === 3 && state.aptitudeAnswers.filter(function(a){ return a !== null; }).length < aptitudeQuestions.length) {
    Toast.show("Please answer all aptitude questions before proceeding.", "error");
    return;
  }
  if (from === 4) savePsychAnswers();
  if (from === 5) saveInterests();
  if (from === 6) {
    saveSkills();
    // For Class 7-12: skip Certifications (7) and Projects (8) — go straight to Results (9)
    if (isSchoolLevel()) {
      state.certs = [];   // no certs
      state.projs = [];   // no projects
      currentStep = 9;
      updateStepUI("next");
      window.scrollTo(0, 0);
      return;
    }
  }
  if (from === 7) saveCerts();

  currentStep = from + 1;
  updateStepUI("next");
  window.scrollTo(0, 0);

  if (currentStep === 3) loadAptitudeQuestions();
  if (currentStep === 4) renderPsychometric();
  if (currentStep === 5) renderInterests();
  if (currentStep === 6) renderSkills();
}

function prevStep(from) {
  // For Class 7-12: skip back over steps 7 and 8
  if ((from === 7 || from === 8 || from === 9) && isSchoolLevel()) {
    currentStep = 6;
  } else {
    currentStep = from - 1;
  }
  updateStepUI("prev");
  window.scrollTo(0, 0);
}


/* -- STEP 1: EDUCATION FIELDS --------------------------------- */
function bindEducationFields() {
  var lvlEl = document.getElementById("education_level");
  var streamGrp  = document.getElementById("stream-group");
  var degreeGrp  = document.getElementById("degree-group");
  var specGrp    = document.getElementById("spec-group");
  var attendGrp  = document.getElementById("attendance-group");
  var cgpaEl     = document.getElementById("cgpa");
  var cgpaLabel  = cgpaEl ? cgpaEl.previousElementSibling : null;

  function updateVisibility() {
    var lvl = lvlEl.value;
    var isJuniorSchool = ["Class 7","Class 8","Class 9","Class 10"].includes(lvl);
    var isSeniorSchool = ["Higher Secondary (11-12)"].includes(lvl);
    var isSchool  = isJuniorSchool || isSeniorSchool;
    var isUG = ["Undergraduate","Postgraduate","Professional Degree","Diploma / ITI"].includes(lvl);
    var isHS = isSeniorSchool;

    // Stream: show for HS and UG
    if (streamGrp) streamGrp.style.display = (isHS || isUG) ? "" : "none";
    // Degree / Specialization: only for UG+
    if (degreeGrp) degreeGrp.style.display = isUG ? "" : "none";
    if (specGrp)   specGrp.style.display   = isUG ? "" : "none";
    // Attendance: hidden for all school levels (7-12)
    if (attendGrp) attendGrp.style.display  = isSchool ? "none" : "";
    // CGPA: hidden for school levels — avg is computed from Step 2 subject marks
    if (cgpaEl) {
      var cgpaGrp = cgpaEl.closest(".form-group");
      if (cgpaGrp) cgpaGrp.style.display = isSchool ? "none" : "";
    }
  }

  lvlEl.addEventListener("change", updateVisibility);
  updateVisibility();
}

/* -- STEP 2: SUBJECT MARKS ------------------------------------ */
function loadSubjectMarks() {
  var edu = state.education;
  var boardSubjMap = BOARD_SUBJECTS[edu.education_level];
  var subjects = [];
  if (boardSubjMap) {
    subjects = boardSubjMap[edu.board] || boardSubjMap[edu.stream] || boardSubjMap["default"] || [];
  }
  if (!subjects.length) subjects = ["Subject 1","Subject 2","Subject 3","Subject 4","Subject 5"];

  // Update subtitle with student's context
  var subtitle = document.getElementById("step2-subtitle");
  if (subtitle) {
    var levelLabel = edu.education_level || "Student";
    var boardLabel = edu.board || "";
    subtitle.textContent = levelLabel + (boardLabel ? " \u2014 " + boardLabel : "") +
      " \u2014 Enter marks for each subject (0\u2013100)";
  }

  var tbody = document.getElementById("subjects-body");
  var isSchool = ["Class 7","Class 8","Class 9","Class 10"].includes(edu.education_level);
  tbody.innerHTML = subjects.map(function(s, i) {
    return "<tr><td>" + s + "</td><td><input type=\"number\" min=\"0\" max=\"100\" step=\"0.5\" placeholder=\"" + (isSchool ? "0-100" : "0-100") + "\" id=\"subj-marks-" + i + "\" /></td><td><select id=\"subj-grade-" + i + "\"><option value=\"\">Grade</option><option>A+</option><option>A</option><option>B+</option><option>B</option><option>C+</option><option>C</option><option>D</option><option>F</option></select></td></tr>";
  }).join("");

  state._subjects = subjects;

  // Update step 6/7/8 UI to reflect school vs college context
  _applySchoolModeUI();
}


function saveSubjectMarks() {
  var subjects = state._subjects || [];
  state.subjectMarks = subjects.map(function(s, i) {
    var marksEl = document.getElementById("subj-marks-" + i);
    var gradeEl = document.getElementById("subj-grade-" + i);
    return {
      subject: s,
      marks: parseFloat(marksEl ? marksEl.value : 0) || 0,
      grade: gradeEl ? gradeEl.value : "",
    };
  });
  // Compute average marks across all entered subjects (skip blank entries)
  var filledMarks = state.subjectMarks.filter(function(m){ return m.marks > 0; });
  state.avgMarks = filledMarks.length > 0
    ? Math.round(filledMarks.reduce(function(s,m){ return s + m.marks; }, 0) / filledMarks.length)
    : 0;
}


/* -- STEP 3: APTITUDE ----------------------------------------- */
async function loadAptitudeQuestions() {
  var loading = document.getElementById("aptitude-loading");
  var container = document.getElementById("aptitude-questions");
  loading.style.display = "flex";
  container.style.display = "none";

  var eduCategory = getEduCategory(state.education.education_level || "Undergraduate");

  // Always use local adaptive bank — the backend API has un-categorised old questions
  // that are not appropriate for the student's education level.
  aptitudeQuestions = selectAptitudeQuestions(eduCategory);

  state.aptitudeAnswers = new Array(aptitudeQuestions.length).fill(null);
  renderAptitudeQuestions();
  loading.style.display = "none";
  container.style.display = "block";
}

function renderAptitudeQuestions() {
  var container = document.getElementById("aptitude-questions");
  var eduCategory = getEduCategory(state.education.education_level || "Undergraduate");
  var config = getAptitudeConfig(eduCategory);

  var lvlLabels = {
    class7to10: "Class 7-10 Level",
    higherSecondary: "Higher Secondary Level",
    diploma: "Diploma / ITI Level",
    ug: "Undergraduate Level",
    pg: "Postgraduate Level",
    professional: "Professional Level",
  };
  var lvlLabel = lvlLabels[eduCategory] || "Standard Level";

  var infoBar = "<div style=\"margin-bottom:1rem;padding:0.7rem 1rem;background:var(--primary-xlight);border-radius:var(--radius-md);border-left:4px solid var(--primary);\"><span style=\"font-size:0.82rem;font-weight:700;color:var(--primary)\">&#128202; " + lvlLabel + " &mdash; " + config.total + " Questions</span><span style=\"font-size:0.78rem;color:var(--text-muted);margin-left:0.75rem\">Easy: " + config.easy + " &middot; Medium: " + config.medium + " &middot; Hard: " + config.hard + "</span></div>";

  container.innerHTML = infoBar + aptitudeQuestions.map(function(q, qi) {
    var opts = ["A","B","C","D"].map(function(letter) {
      var text = q["option_" + letter.toLowerCase()];
      if (!text) return "";
      return "<button class=\"option-btn\" data-q=\"" + qi + "\" data-ans=\"" + letter + "\" onclick=\"selectAptitude(" + qi + ",'" + letter + "',this)\"><span class=\"option-label\">" + letter + ".</span> " + text + "</button>";
    }).join("");
    return "<div class=\"card mb-3\" style=\"border-left:3px solid var(--primary)\"><div class=\"q-counter\">Question " + (qi+1) + " of " + aptitudeQuestions.length + " &middot; <span class=\"badge badge-primary\">" + (q.category||"Reasoning") + "</span> &middot; <span class=\"badge badge-amber\">" + (q.difficulty||"Medium") + "</span></div><div class=\"q-text\">" + q.question_text + "</div><div class=\"options-grid\" id=\"apt-opts-" + qi + "\">" + opts + "</div></div>";
  }).join("");

  checkAptitudeComplete();
}

function selectAptitude(qi, letter, btn) {
  state.aptitudeAnswers[qi] = letter;
  document.querySelectorAll("#apt-opts-" + qi + " .option-btn").forEach(function(b) {
    b.style.borderColor = "";
    b.style.background = "";
    b.style.color = "";
  });
  btn.style.borderColor = "var(--primary)";
  btn.style.background = "var(--badge-bg)";
  btn.style.color = "var(--badge-text)";
  checkAptitudeComplete();
}

function checkAptitudeComplete() {
  var answered = state.aptitudeAnswers.filter(function(a){ return a !== null; }).length;
  var nextBtn = document.getElementById("aptitude-next-btn");
  if (nextBtn) nextBtn.style.display = answered === aptitudeQuestions.length ? "inline-flex" : "none";
}

/* -- STEP 4: PSYCHOMETRIC ------------------------------------- */
function renderPsychometric() {
  var container = document.getElementById("psych-container");
  var eduCategory = getEduCategory(state.education.education_level || "Undergraduate");
  var pool = PSYCH_BANK[eduCategory] || PSYCH_BANK.ug;
  var count = getPsychCount(eduCategory);

  psychScenarios = [...pool].sort(function(){ return Math.random() - 0.5; }).slice(0, count);
  state.psychAnswers = new Array(psychScenarios.length).fill(null);

  container.innerHTML = psychScenarios.map(function(sc, si) {
    var opts = sc.options.map(function(opt, oi) {
      return "<button class=\"option-btn\" data-si=\"" + si + "\" data-oi=\"" + oi + "\" onclick=\"selectPsych(" + si + "," + oi + ",this)\"><span class=\"option-label\">" + String.fromCharCode(65+oi) + ".</span> " + opt.label + "</button>";
    }).join("");
    return "<div class=\"card mb-3\" style=\"border-left:3px solid var(--violet)\"><div class=\"q-counter\">Scenario " + (si+1) + " of " + psychScenarios.length + "</div><div class=\"q-text\">" + sc.q + "</div><div class=\"options-grid\" id=\"psych-opts-" + si + "\">" + opts + "</div></div>";
  }).join("");
}

function selectPsych(si, oi, btn) {
  state.psychAnswers[si] = oi;
  document.querySelectorAll("#psych-opts-" + si + " .option-btn").forEach(function(b) {
    b.style.borderColor = "";
    b.style.background = "";
    b.style.color = "";
  });
  btn.style.borderColor = "var(--violet)";
  btn.style.background = "rgba(139,92,246,0.1)";
  btn.style.color = "var(--violet)";
}

function savePsychAnswers() {
  var traits = {};
  psychScenarios.forEach(function(sc, si) {
    var selected = state.psychAnswers[si];
    if (selected === null) return;
    var opt = sc.options[selected];
    Object.entries(opt.traits).forEach(function(entry) {
      traits[entry[0]] = (traits[entry[0]] || 0) + entry[1];
    });
  });
  state.psychTraits = traits;
}

/* -- STEP 5: INTEREST PAIRS ----------------------------------- */
function renderInterests() {
  var container = document.getElementById("interest-container");
  interestPairs = [...INTEREST_BANK].sort(function(){ return Math.random() - 0.5; }).slice(0, 8);
  state._interestAnswers = new Array(interestPairs.length).fill(null);

  container.innerHTML = interestPairs.map(function(pair, pi) {
    return "<div class=\"mb-4\"><p style=\"font-weight:700;color:var(--text-h);margin-bottom:0.75rem;font-size:0.95rem\">" + (pi+1) + ". " + pair.q + "</p><div class=\"interest-pair\" id=\"int-pair-" + pi + "\"><button class=\"interest-option\" data-pi=\"" + pi + "\" data-opt=\"a\" onclick=\"selectInterest(" + pi + ",'a',this)\">" + pair.a.label + "</button><button class=\"interest-option\" data-pi=\"" + pi + "\" data-opt=\"b\" onclick=\"selectInterest(" + pi + ",'b',this)\">" + pair.b.label + "</button></div></div>";
  }).join("");
}

function selectInterest(pi, opt, btn) {
  var alreadySelected = btn.classList.contains("selected");
  document.querySelectorAll("#int-pair-" + pi + " .interest-option").forEach(function(b) {
    b.classList.remove("selected");
    b.setAttribute("aria-pressed","false");
  });
  if (alreadySelected) {
    state._interestAnswers[pi] = null;
  } else {
    btn.classList.add("selected");
    btn.setAttribute("aria-pressed","true");
    state._interestAnswers[pi] = opt;
  }
}

function saveInterests() {
  var scores = {};
  interestPairs.forEach(function(pair, pi) {
    var chosen = state._interestAnswers[pi];
    if (!chosen) return;
    var domains = chosen === "a" ? pair.a.domains : pair.b.domains;
    Object.entries(domains).forEach(function(entry) {
      scores[entry[0]] = (scores[entry[0]] || 0) + entry[1];
    });
  });
  state.interestScores = scores;
}

/* -- STEP 6: SKILLS ------------------------------------------- */
function renderSkills() {
  var grid = document.getElementById("skill-grid");
  if (!grid) return;

  grid.innerHTML = ALL_SKILLS.map(function(skill) {
    var safeKey = skill.replace(/[^a-zA-Z0-9]/g,"_");
    var hasQuiz = !!SKILL_QUIZ_BANK[skill];
    return "<div class=\"skill-chip-wrapper\" id=\"sw-" + safeKey + "\"><div class=\"skill-chip\" data-skill=\"" + skill + "\" onclick=\"onSkillClick(this.getAttribute('data-skill'))\"><span class=\"skill-name\">" + skill + "</span><span class=\"skill-level-badge\" id=\"slb-" + safeKey + "\" style=\"display:none\"></span>" + (hasQuiz ? "<span style=\"font-size:0.55rem;color:var(--primary);margin-left:3px\" title=\"Quiz available\">&#128221;</span>" : "") + "</div><div class=\"skill-score-tag\" id=\"sst-" + safeKey + "\" style=\"display:none;font-size:0.6rem;color:var(--text-muted);text-align:center;margin-top:2px\"></div></div>";
  }).join("");
}

function onSkillClick(skill) {
  var chip = document.querySelector(".skill-chip[data-skill=\"" + skill + "\"]");
  var isSelected = chip && chip.classList.contains("selected");

  if (isSelected) {
    if (chip) chip.classList.remove("selected");
    state.selectedSkills = state.selectedSkills.filter(function(s){ return s !== skill; });
    delete state_skillProficiency[skill];
    var safeKey = skill.replace(/[^a-zA-Z0-9]/g,"_");
    var badge = document.getElementById("slb-" + safeKey);
    var scoreTag = document.getElementById("sst-" + safeKey);
    if (badge) badge.style.display = "none";
    if (scoreTag) scoreTag.style.display = "none";
  } else {
    openSkillQuiz(skill);
  }
}

function saveSkills() {
  state.skillsWithLevel = state.selectedSkills.map(function(s) {
    return { skill: s, proficiency: state_skillProficiency[s] || "Beginner" };
  });
}

/* -- STEP 7: CERTIFICATIONS ----------------------------------- */
function addCert() {
  var container = document.getElementById("certs-container");
  var i = certCount++;
  var row = document.createElement("div");
  row.className = "cert-row";
  row.id = "cert-" + i;
  row.innerHTML = "<div class=\"form-group\"><label>Certification Name</label><input type=\"text\" placeholder=\"e.g. AWS Cloud Practitioner\" id=\"cert-name-" + i + "\" /></div><div class=\"form-group\"><label>Provider</label><input type=\"text\" placeholder=\"e.g. Amazon, Google\" id=\"cert-provider-" + i + "\" /></div><button class=\"btn btn-danger btn-sm\" onclick=\"removeCert(" + i + ")\" style=\"height:40px;align-self:flex-end\">&times;</button>";
  container.appendChild(row);
}

function removeCert(i) {
  var el = document.getElementById("cert-" + i);
  if (el) el.remove();
}

function saveCerts() {
  state.certs = [];
  document.querySelectorAll("[id^=\"cert-name-\"]").forEach(function(el) {
    var i = el.id.split("-").pop();
    var name = el.value.trim();
    var provEl = document.getElementById("cert-provider-" + i);
    var prov = provEl ? provEl.value.trim() : "";
    if (name) state.certs.push({ name: name, provider: prov });
  });
}

/* -- STEP 8: PROJECTS ----------------------------------------- */
function addProj() {
  var container = document.getElementById("projs-container");
  var i = projCount++;
  var row = document.createElement("div");
  row.className = "proj-row";
  row.id = "proj-" + i;
  row.innerHTML = "<div class=\"form-group\"><label>Project Title</label><input type=\"text\" placeholder=\"e.g. E-Commerce Platform\" id=\"proj-title-" + i + "\" /></div><div class=\"form-group\"><label>Technologies Used</label><input type=\"text\" placeholder=\"e.g. React, Python\" id=\"proj-tech-" + i + "\" /></div><button class=\"btn btn-danger btn-sm\" onclick=\"removeProj(" + i + ")\" style=\"height:40px;align-self:flex-end\">&times;</button>";
  container.appendChild(row);
}

function removeProj(i) {
  var el = document.getElementById("proj-" + i);
  if (el) el.remove();
}

function saveProjects() {
  state.projs = [];
  document.querySelectorAll("[id^=\"proj-title-\"]").forEach(function(el) {
    var i = el.id.split("-").pop();
    var title = el.value.trim();
    var techEl = document.getElementById("proj-tech-" + i);
    var tech = techEl ? techEl.value.trim() : "";
    if (title) state.projs.push({ title: title, technology: tech });
  });
}

/* -- SUBMIT ASSESSMENT ---------------------------------------- */
async function submitAssessment() {
  saveCerts();
  saveProjects();
  saveSkills();

  var submitBtn = document.getElementById("submit-assessment-btn");
  if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = "&#8987; Analysing..."; }

  currentStep = 9;
  updateStepUI("next");
  window.scrollTo(0, 0);

  var correct = state.aptitudeAnswers.filter(function(ans, i) {
    var q = aptitudeQuestions[i];
    return q && ans === q.correct_answer;
  }).length;
  var aptitudePct = aptitudeQuestions.length > 0 ? Math.round((correct / aptitudeQuestions.length) * 100) : 70;

  var topInterestEntry = Object.entries(state.interestScores).sort(function(a,b){ return b[1]-a[1]; })[0];
  var topInterest = topInterestEntry ? topInterestEntry[0].replace(/_/g," ") : "Technology";

  // Use avg_marks computed in saveSubjectMarks (skips blank entries)
  // state.avgMarks is set when Step 2 is saved; fallback to 75 if no marks entered
  var avgMarks = state.avgMarks > 0 ? state.avgMarks : 75;

  // For school students: derive sensible ML features since CGPA/Attendance fields are hidden
  var eduLevel = state.education.education_level || "Undergraduate";
  var schoolYearMap = {
    "Class 7": 1, "Class 8": 2, "Class 9": 3, "Class 10": 4,
    "Higher Secondary (11-12)": 5, "Diploma / ITI": 2
  };
  var isSchoolStudent = isSchoolLevel();
  // CGPA for school: convert percentage to 10-point scale (e.g. 85% → 8.5)
  var cgpaValue = isSchoolStudent
    ? parseFloat((avgMarks / 10).toFixed(1))
    : (state.education.cgpa || 0);
  // Year of study: use class-mapped value for school, default 2 for others
  var yearOfStudy = schoolYearMap[eduLevel] || (state.education.year_of_study || 2);
  // Attendance: school students default to 85 (not collected), college uses entered value
  var attendancePct = isSchoolStudent ? 85 : (state.education.attendance || 80);

  var payload = {
    education_level: eduLevel,
    board: state.education.board || "CBSE",
    stream: state.education.stream || "General",
    degree: state.education.degree || "",
    specialization: state.education.specialization || "",
    cgpa: cgpaValue,
    attendance_pct: attendancePct,
    year_of_study: yearOfStudy,
    avg_marks: avgMarks,
    logical_aptitude: aptitudePct,
    numerical_ability: aptitudePct,
    verbal_ability: aptitudePct,
    programming_score: state.selectedSkills.some(function(s){ return ["Programming","Machine Learning","Data Analysis","SQL & Databases"].includes(s); }) ? 80 : 40,
    skills: state.selectedSkills,
    skills_with_level: state.skillsWithLevel || [],
    certifications: state.certs,
    projects: state.projs,
    psychometric_traits: state.psychTraits,
    interest_domain: topInterest,
    interest_scores: state.interestScores,
    subject_marks: state.subjectMarks,
  };


  try {
    var user = Auth.getUser();
    var res = await API.post("/api/assessment/submit", Object.assign({}, payload, { user_id: user ? user.id : null }), true);
    renderResults(res);
    Toast.show("Assessment complete! Your career recommendations are ready.", "success");
  } catch(err) {
    console.error(err);
    renderResults({
      top5_careers: [
        { rank:1, career:"Software Developer", confidence:88, why:["Strong Analytical Thinking","Technology Interest","Problem Solving Aptitude"], salary:"Rs.5L-Rs.18L/yr", degree:"BTech CS / BCA", companies:"Infosys, TCS, Google", growth:"+22% annually", certifications:"AWS, Full Stack Cert" },
        { rank:2, career:"Data Analyst", confidence:82, why:["Quantitative Skills","Analytical Mindset","Attention to Detail"], salary:"Rs.4L-Rs.14L/yr", degree:"BTech / BSc Statistics", companies:"Wipro, Accenture", growth:"+25% annually", certifications:"Google Data Analytics" },
        { rank:3, career:"Business Analyst", confidence:76, why:["Logical Reasoning","Communication Skills","Structured Thinking"], salary:"Rs.5L-Rs.15L/yr", degree:"BBA / BTech / MBA", companies:"Deloitte, EY, KPMG", growth:"+20% annually", certifications:"PMP, BA Cert" },
        { rank:4, career:"Machine Learning Engineer", confidence:70, why:["Mathematical Aptitude","Technology Curiosity","Problem Solving"], salary:"Rs.8L-Rs.25L/yr", degree:"BTech CS / MTech AI", companies:"Google, Microsoft, Amazon", growth:"+28% annually", certifications:"TensorFlow, AWS ML" },
        { rank:5, career:"School Teacher", confidence:65, why:["Communication Skills","Patience","Subject Knowledge"], salary:"Rs.3L-Rs.9L/yr", degree:"BA / BSc + B.Ed", companies:"Government Schools, Ed-Tech", growth:"+12% annually", certifications:"CTET, TET" },
      ],
      readiness_score: Math.round((aptitudePct + avgMarks) / 2),
      status: "success"
    });
    Toast.show("Showing demo results (server not available).", "info");
  } finally {
    if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = "&#129302; Get AI Career Prediction &rarr;"; }
  }
}

/* -- RESULTS RENDERING ---------------------------------------- */
function renderResults(res) {
  var top5 = res.top5_careers || [];
  var readiness = Math.round(res.readiness_score || 0);
  var readColor = readiness >= 80 ? "var(--emerald)" : readiness >= 60 ? "var(--amber)" : "var(--red)";

  if (top5.length) {
    localStorage.setItem("top5Careers", JSON.stringify(top5));
    localStorage.setItem("readinessScore", readiness);
    localStorage.setItem("finalRecommendedCareer", top5[0].career);
  }

  var container = document.getElementById("results-content");
  var html = "<div class=\"text-center mb-4\"><div style=\"font-size:3rem;margin-bottom:0.5rem\">&#127881;</div><h2 style=\"font-size:1.75rem;font-weight:900;color:var(--text-h);margin-bottom:0.5rem\">Assessment Complete!</h2><p style=\"color:var(--text-muted)\">Your AI-powered career analysis is ready</p><div style=\"margin-top:1rem;display:inline-flex;flex-direction:column;align-items:center;gap:0.25rem\"><span style=\"font-size:0.78rem;color:var(--text-muted);font-weight:700;text-transform:uppercase\">Career Readiness Index</span><span style=\"font-size:2.5rem;font-weight:900;color:" + readColor + "\">" + readiness + "%</span></div></div>";

  top5.forEach(function(c, idx) {
    var skillsHtml = "";
    if (CAREER_SKILL_MAP[c.career]) {
      skillsHtml = "<div style=\"margin-top:0.75rem\"><span style=\"font-size:0.75rem;color:var(--text-muted);font-weight:700\">KEY SKILLS:</span><div class=\"flex gap-1 wrap mt-1\">" + CAREER_SKILL_MAP[c.career].map(function(sk){ return "<span class=\"badge badge-primary\">" + sk + "</span>"; }).join("") + "</div></div>";
    }
    var whyBadges = (c.why||[]).map(function(w){ return "<span class=\"badge badge-emerald\">&#10003; " + w + "</span>"; }).join("");
    var fillColor = idx === 0 ? "var(--gradient-primary)" : "rgba(99,102,241,0.4)";
    var rankColor = idx === 0 ? "var(--text-link)" : "var(--text-h)";
    html += "<div class=\"career-card " + (idx === 0 ? "top-match" : "") + " mb-3\">" + (idx === 0 ? "<span class=\"top-match-label\">#1 TOP MATCH</span>" : "") + "<div class=\"flex justify-between items-center wrap gap-2 mb-2\"><div><span class=\"career-rank\">#" + (c.rank||idx+1) + "</span><strong style=\"color:var(--text-h);font-size:1.05rem\">" + c.career + "</strong></div><div style=\"font-size:1.75rem;font-weight:900;color:" + rankColor + "\">" + c.confidence + "%</div></div><div class=\"flex gap-1 wrap mb-2\">" + whyBadges + "</div><div class=\"progress-bar mb-2\"><div class=\"progress-fill\" style=\"width:" + c.confidence + "%;background:" + fillColor + "\"></div></div><div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0.6rem;font-size:0.82rem\"><div><span style=\"color:var(--text-muted)\">&#128176; Salary:</span> <strong>" + (c.salary||"&mdash;") + "</strong></div><div><span style=\"color:var(--text-muted)\">&#127891; Degree:</span> <strong>" + (c.degree||"&mdash;") + "</strong></div><div><span style=\"color:var(--text-muted)\">&#127970; Companies:</span> <strong>" + (c.companies||"&mdash;") + "</strong></div><div><span style=\"color:var(--text-muted)\">&#128200; Growth:</span> <strong>" + (c.growth||"&mdash;") + "</strong></div></div>" + skillsHtml + "</div>";
  });

  html += "<div class=\"flex gap-2 justify-center mt-4 wrap\"><a href=\"/dashboard.html\" class=\"btn btn-primary btn-lg\">View Full Dashboard &rarr;</a><a href=\"/assessment.html\" class=\"btn btn-secondary btn-lg\">Retake Assessment</a></div>";

  container.innerHTML = html;
}

/* -- SKILL QUIZ MODAL ----------------------------------------- */
var _quizSkill = null;
var _quizAnswers = [];
var _quizTotal   = 0;

// Self-rating for skills without a dedicated quiz
function _showSelfRating(skill) {
  var modal = document.getElementById("skill-quiz-modal");
  var title = document.getElementById("sqm-title");
  var body  = document.getElementById("sqm-body");
  var submitBtn = document.getElementById("sqm-submit");

  title.textContent = "Rate Your Level: " + skill;
  submitBtn.style.display = "none";

  var levels = [
    { level:"Beginner",     icon:"📗", desc:"I have basic awareness or have used this occasionally." },
    { level:"Intermediate", icon:"📘", desc:"I use this regularly and understand core concepts." },
    { level:"Advanced",     icon:"📙", desc:"I am highly proficient and use this in complex situations." },
  ];
  body.innerHTML = "<p style=\"color:var(--text-muted);font-size:0.85rem;margin-bottom:1rem\">No quiz available for this skill. Please rate your own proficiency honestly:</p>" +
    levels.map(function(l) {
      return "<button class=\"sqm-opt-btn\" style=\"margin-bottom:0.5rem;text-align:left\" onclick=\"_applySelfRating('" + skill + "','" + l.level + "')\">" +
        "<span style=\"font-size:1.1rem;margin-right:0.5rem\">" + l.icon + "</span>" +
        "<strong>" + l.level + "</strong>" +
        "<span style=\"display:block;font-size:0.77rem;color:var(--text-muted);margin-top:2px;margin-left:1.6rem\">" + l.desc + "</span>" +
        "</button>";
    }).join("");

  modal.style.display = "flex";
  setTimeout(function(){ modal.classList.add("show"); }, 10);
}

function _applySelfRating(skill, level) {
  closeSkillQuiz();
  applySkillVerification(skill, level, 0, 0);
}

function openSkillQuiz(skill) {
  var questions = SKILL_QUIZ_BANK[skill];
  if (!questions || !questions.length) {
    // No quiz available: show a self-rating modal instead of silently adding as Beginner
    _showSelfRating(skill);
    return;
  }
  _quizSkill   = skill;
  _quizAnswers = new Array(questions.length).fill(null);
  _quizTotal   = questions.length;

  var modal = document.getElementById("skill-quiz-modal");
  var title = document.getElementById("sqm-title");
  var body  = document.getElementById("sqm-body");
  var submitBtn = document.getElementById("sqm-submit");

  title.textContent = "Skill Check: " + skill;
  submitBtn.style.display = "none";

  body.innerHTML = questions.map(function(q, qi) {
    var opts = q.opts.map(function(opt, oi) {
      return "<button class=\"sqm-opt-btn\" id=\"sqm-opt-" + qi + "-" + oi + "\" onclick=\"selectSkillQuizOpt(" + qi + "," + oi + "," + q.ans + ")\"><span class=\"sqm-opt-letter\">" + ["A","B","C","D"][oi] + "</span>" + opt + "</button>";
    }).join("");
    return "<div class=\"sqm-question\" id=\"sqm-q" + qi + "\"><div class=\"sqm-q-label\">Q" + (qi+1) + " of " + questions.length + "</div><div class=\"sqm-q-text\">" + q.q + "</div><div class=\"sqm-options\">" + opts + "</div></div>";
  }).join("<hr style=\"border:none;border-top:1px solid var(--border);margin:0.75rem 0\">");

  modal.style.display = "flex";
  setTimeout(function(){ modal.classList.add("show"); }, 10);
}

function selectSkillQuizOpt(qi, oi, correctOi) {
  _quizAnswers[qi] = oi;

  document.querySelectorAll("#sqm-q" + qi + " .sqm-opt-btn").forEach(function(b, idx) {
    b.classList.remove("sqm-selected","sqm-correct","sqm-wrong");
    if (idx === correctOi) b.classList.add("sqm-correct");
    else if (idx === oi && oi !== correctOi) b.classList.add("sqm-wrong");
    b.disabled = true;
  });

  var allAnswered = _quizAnswers.every(function(a){ return a !== null; });
  if (allAnswered) {
    var submitBtn = document.getElementById("sqm-submit");
    submitBtn.style.display = "inline-flex";
    submitBtn.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function submitSkillQuiz() {
  var questions = SKILL_QUIZ_BANK[_quizSkill];
  var score = 0;
  _quizAnswers.forEach(function(ans, i){ if (ans === questions[i].ans) score++; });

  var level = "Beginner";
  if (score === _quizTotal) level = "Advanced";
  else if (score >= Math.ceil(_quizTotal / 2)) level = "Intermediate";

  var body = document.getElementById("sqm-body");
  var icons = { Beginner:"&#127993;", Intermediate:"&#127992;", Advanced:"&#127994;" };
  var msgs  = {
    Beginner:     "Keep learning! You have foundational awareness.",
    Intermediate: "Good understanding! You know the core concepts.",
    Advanced:     "Excellent! You have strong command of this skill.",
  };
  body.innerHTML = "<div style=\"text-align:center;padding:1.5rem 0\"><div style=\"font-size:3rem;margin-bottom:0.5rem\">" + icons[level] + "</div><div style=\"font-size:1.4rem;font-weight:800;color:var(--text-h);margin-bottom:0.25rem\">" + score + " / " + _quizTotal + " Correct</div><div style=\"font-size:1rem;font-weight:700;color:var(--primary);margin-bottom:0.5rem\">Proficiency: " + level + "</div><div style=\"font-size:0.85rem;color:var(--text-muted)\">" + msgs[level] + "</div></div>";
  document.getElementById("sqm-submit").style.display = "none";

  setTimeout(function() {
    closeSkillQuiz();
    applySkillVerification(_quizSkill, level, score, _quizTotal);
  }, 1800);
}

function closeSkillQuiz() {
  var modal = document.getElementById("skill-quiz-modal");
  modal.classList.remove("show");
  setTimeout(function(){ modal.style.display = "none"; }, 250);
}

function applySkillVerification(skill, level, score, total) {
  var safeKey = skill.replace(/[^a-zA-Z0-9]/g,"_");
  var chip  = document.querySelector(".skill-chip[data-skill=\"" + skill + "\"]");
  var badge = document.getElementById("slb-" + safeKey);

  state_skillProficiency[skill] = level;
  if (!state.selectedSkills.includes(skill)) state.selectedSkills.push(skill);

  if (chip) chip.classList.add("selected");

  var colors     = { Beginner:"rgba(245,158,11,0.15)", Intermediate:"rgba(99,102,241,0.15)", Advanced:"rgba(16,185,129,0.15)" };
  var textColors = { Beginner:"var(--amber)", Intermediate:"var(--primary)", Advanced:"var(--emerald)" };
  var checkIcons = { Beginner:"&#128216;", Intermediate:"&#128215;", Advanced:"&#11088;" };

  if (badge) {
    badge.innerHTML = checkIcons[level] + " " + level;
    badge.style.display  = "inline-block";
    badge.style.background  = colors[level];
    badge.style.color       = textColors[level];
    badge.style.padding     = "2px 7px";
    badge.style.borderRadius= "10px";
    badge.style.fontSize    = "0.62rem";
    badge.style.fontWeight  = "700";
    badge.style.marginLeft  = "4px";
  }

  if (total > 0) {
    var scoreTag = document.getElementById("sst-" + safeKey);
    if (scoreTag) {
      scoreTag.textContent = score + "/" + total + " correct";
      scoreTag.style.display = "block";
    }
  }
  Toast.show(skill + " added - " + level + " level", "success");
}

/* -- INIT ----------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function() {
  ThemeManager.init();
  Toast.init();
  renderNavbar("assessment");
  if (!Auth.requireAuth()) return;
  renderStepNav();
  bindEducationFields();
});
