from __future__ import annotations

from source_items import Item


def item(
    question: str,
    correct: str,
    wrong: str,
    distractor_1: str,
    distractor_2: str,
    note: str,
) -> Item:
    return Item(
        question,
        correct,
        wrong,
        distractor_1,
        distractor_2,
        note,
    )


def build_easy_items() -> list[Item]:
    rows = [
        ("Which blood component primarily carries oxygen?", "Red blood cells", "White blood cells", "Platelets", "Plasma proteins", "Hemoglobin in red blood cells binds and transports oxygen."),
        ("Which chamber pumps oxygenated blood into the aorta?", "Left ventricle", "Right ventricle", "Left atrium", "Right atrium", "The left ventricle sends oxygenated blood into systemic circulation through the aorta."),
        ("Where does most nutrient absorption occur in the human digestive system?", "Small intestine", "Stomach", "Large intestine", "Esophagus", "Villi in the small intestine absorb most digested nutrients."),
        ("Which body system includes the brain and spinal cord?", "Nervous system", "Endocrine system", "Digestive system", "Lymphatic system", "The brain and spinal cord form the central nervous system."),
        ("Which organ produces bile?", "Liver", "Gallbladder", "Pancreas", "Kidney", "The liver produces bile; the gallbladder stores and concentrates it."),
        ("What is the main function of platelets?", "Helping blood clot", "Carrying oxygen", "Producing insulin", "Digesting fats", "Platelets aggregate and support blood clot formation."),
        ("Which molecule stores hereditary information in most organisms?", "DNA", "ATP", "Glucose", "Cellulose", "DNA contains the hereditary sequence information in most organisms."),
        ("Which cell structure controls what enters and leaves a cell?", "Cell membrane", "Nucleolus", "Chromosome", "Vacuole", "The selectively permeable cell membrane regulates transport into and out of the cell."),
        ("Which organelle modifies and packages many proteins for transport?", "Golgi apparatus", "Lysosome", "Centrosome", "Cell wall", "The Golgi apparatus modifies, sorts, and packages proteins."),
        ("Which structures assemble amino acids into proteins?", "Ribosomes", "Mitochondria", "Chloroplasts", "Vacuoles", "Ribosomes translate messenger RNA and assemble proteins."),
        ("What type of organism makes its own food from inorganic materials?", "Autotroph", "Heterotroph", "Decomposer only", "Parasite", "Autotrophs synthesize organic food from inorganic sources using light or chemical energy."),
        ("Which relationship benefits both participating species?", "Mutualism", "Parasitism", "Predation", "Competition", "In mutualism, both species receive a benefit."),
        ("What name is given to an organism's role in its ecosystem?", "Ecological niche", "Population size", "Genotype", "Trophic pyramid", "An ecological niche describes how an organism uses resources and interacts in its environment."),
        ("Which process produces genetically identical daughter cells for growth?", "Mitosis", "Meiosis", "Fertilization", "Mutation", "Mitosis produces two daughter cells with the same chromosome complement."),
        ("Which process forms eggs and sperm with half the usual chromosome number?", "Meiosis", "Mitosis", "Binary fission", "Budding", "Meiosis produces haploid gametes."),
        ("In a typical food web, what do arrows usually show?", "Direction of energy transfer", "Direction animals travel", "Relative body size", "Amount of rainfall", "Food-web arrows point from the consumed organism toward the consumer, showing energy transfer."),
        ("What is an animal without a backbone called?", "Invertebrate", "Vertebrate", "Amphibian", "Mammal", "Invertebrates lack a vertebral column."),
        ("Which plant tissue transports water upward from roots?", "Xylem", "Phloem", "Epidermis", "Cambium only", "Xylem conducts water and dissolved minerals from roots."),
        ("Which plant tissue transports sugars from photosynthetic tissues?", "Phloem", "Xylem", "Cork", "Root hair", "Phloem distributes sugars and other organic products."),
        ("What is the opening in a leaf that regulates gas exchange called?", "Stoma", "Sepal", "Anther", "Node", "Stomata are pores controlled by guard cells."),
        ("Which macromolecule is built from amino acids?", "Protein", "Carbohydrate", "Nucleic acid", "Lipid", "Amino acids link together to form proteins."),
        ("Which macromolecules include fats and oils?", "Lipids", "Proteins", "Minerals", "Nucleic acids", "Fats and oils are types of lipids."),
        ("What is the immediate usable energy-carrying molecule in cells?", "ATP", "DNA", "Starch", "Cholesterol", "Cells commonly couple energy-requiring reactions to ATP breakdown."),
        ("Which immune cells can produce antibodies?", "B lymphocytes", "Red blood cells", "Platelets", "Bone cells", "Activated B lymphocytes differentiate into plasma cells that secrete antibodies."),
        ("Which part of a neuron usually receives signals from other cells?", "Dendrites", "Axon terminal", "Myelin only", "Cell membrane pump", "Dendrites are specialized to receive incoming signals."),
        ("What is the chemical symbol for sodium?", "Na", "S", "So", "N", "Sodium's symbol is Na, derived from natrium."),
        ("What is the chemical symbol for potassium?", "K", "P", "Po", "Pt", "Potassium's chemical symbol is K."),
        ("Which element has the chemical symbol Fe?", "Iron", "Fluorine", "Francium", "Fermium", "Fe is the chemical symbol for iron."),
        ("Which element has the chemical symbol Ag?", "Silver", "Argon", "Gold", "Aluminum", "Ag, from argentum, is the symbol for silver."),
        ("What is the formula of carbon dioxide?", "CO2", "CO", "C2O", "O2C2", "A carbon dioxide molecule contains one carbon atom and two oxygen atoms."),
        ("What is the formula of methane?", "CH4", "CH3", "C2H4", "H4O", "Methane contains one carbon atom bonded to four hydrogen atoms."),
        ("Which subatomic particle has a negative electric charge?", "Electron", "Proton", "Neutron", "Photon", "An electron carries one negative elementary charge."),
        ("Which subatomic particle determines an element's atomic number?", "Proton", "Neutron", "Electron shell", "Photon", "Atomic number equals the number of protons in the nucleus."),
        ("Where are protons and neutrons located in an atom?", "Nucleus", "Electron cloud only", "Chemical bond", "Outer shell only", "Protons and neutrons occupy the atomic nucleus."),
        ("What type of bond involves sharing electron pairs?", "Covalent bond", "Ionic bond", "Metallic density", "Nuclear bond", "Covalent bonds form through shared electron pairs."),
        ("What type of ion has gained electrons?", "Anion", "Cation", "Isotope", "Neutron", "Gaining electrons gives an ion a net negative charge, making it an anion."),
        ("A solution with pH 3 is best described as what?", "Acidic", "Neutral", "Basic", "Saturated", "A pH below 7 is acidic."),
        ("A solution with pH 9 is best described as what?", "Basic", "Acidic", "Neutral", "Radioactive", "A pH above 7 is basic."),
        ("Which feature distinguishes plasma from an ordinary neutral gas?", "It contains many free charged particles", "It has a fixed shape", "It has a fixed volume", "It contains no particles", "Plasma is an ionized gas containing mobile ions and electrons."),
        ("Which change of state turns a liquid into a gas at its surface?", "Evaporation", "Condensation", "Freezing", "Deposition", "Evaporation is vaporization occurring at a liquid's surface."),
        ("Which change of state turns a gas directly into a solid?", "Deposition", "Sublimation", "Melting", "Boiling", "Deposition is the direct gas-to-solid transition."),
        ("Which property measures mass per unit volume?", "Density", "Temperature", "Pressure", "Conductivity", "Density is defined as mass divided by volume."),
        ("Which type of mixture has visibly distinct components?", "Heterogeneous mixture", "Homogeneous solution", "Pure element", "Single compound", "A heterogeneous mixture is nonuniform and has distinguishable regions or components."),
        ("What does a catalyst do in a chemical reaction?", "Lowers activation energy", "Raises the reaction's final energy", "Changes the equilibrium products permanently", "Adds mass to every product", "A catalyst provides a lower-activation-energy reaction pathway."),
        ("Which law states that total mass is conserved in a closed chemical reaction?", "Conservation of mass", "Ohm's law", "Boyle's law", "Law of reflection", "In a closed system, chemical reactions rearrange matter without changing total mass."),
        ("Which quantity is measured in newtons?", "Force", "Energy", "Power", "Electric charge", "The SI unit of force is the newton."),
        ("The joule is the SI unit used for which physical quantity?", "Energy", "Force", "Power", "Frequency", "The joule is the SI unit of energy and work."),
        ("Which quantity is measured in watts?", "Power", "Energy", "Voltage", "Mass", "A watt is one joule per second, the SI unit of power."),
        ("What type of energy is associated with motion?", "Kinetic energy", "Chemical element", "Elastic force", "Rest mass only", "Kinetic energy is the energy an object has because it is moving."),
        ("What type of energy is stored in a stretched spring?", "Elastic potential energy", "Kinetic energy", "Nuclear radiation", "Thermal equilibrium", "A deformed elastic object stores elastic potential energy."),
        ("What force opposes relative motion between touching surfaces?", "Friction", "Buoyancy", "Magnetism", "Gravity only", "Friction acts against relative sliding or attempted sliding at a contact."),
        ("What force causes an object immersed in fluid to experience an upward push?", "Buoyant force", "Frictional force", "Tension", "Centripetal force", "Pressure differences in a fluid produce an upward buoyant force."),
        ("Which simple machine is a rigid bar that pivots around a fulcrum?", "Lever", "Pulley only", "Wheel and axle", "Inclined plane", "A lever is a rigid bar rotating about a fulcrum."),
        ("What kind of lens is thicker at the center than at the edges?", "Convex lens", "Concave lens", "Plane mirror", "Prism only", "A convex lens is thicker at its center and converges parallel light."),
        ("What happens to the frequency of a wave when its period increases?", "Frequency decreases", "Frequency increases", "Frequency stays identical in every case", "Frequency becomes zero immediately", "Frequency and period are reciprocals, so increasing period lowers frequency."),
        ("Which electromagnetic waves have longer wavelengths than visible light?", "Infrared waves", "Ultraviolet waves", "X-rays", "Gamma rays", "Infrared lies beyond red light at longer wavelengths."),
        ("Which circuit component is designed to oppose electric current?", "Resistor", "Battery", "Switch only", "Ammeter", "A resistor provides electrical resistance."),
        ("Which material property describes opposition to electric current?", "Electrical resistance", "Electric charge", "Magnetic pole", "Mass density only", "Electrical resistance quantifies how strongly a component opposes current."),
        ("What is the SI unit of electric current?", "Ampere", "Volt", "Ohm", "Coulomb per kilogram", "The ampere is the SI base unit of electric current."),
        ("What is the SI unit of frequency?", "Hertz", "Watt", "Pascal", "Tesla per second", "One hertz is one cycle per second."),
        ("Which seismic wave can travel through both solids and liquids?", "P-wave", "S-wave", "Surface wave only", "Ocean wave", "Compressional P-waves propagate through solids and fluids."),
        ("What is the name of Earth's molten iron-nickel layer surrounding the inner core?", "Outer core", "Inner core", "Crust", "Upper mantle only", "Earth's outer core is a liquid iron-nickel layer."),
        ("Which rock type forms when magma or lava cools?", "Igneous rock", "Sedimentary rock", "Metamorphic rock", "Organic soil", "Cooling and solidification of molten rock produces igneous rock."),
        ("Which rock type forms from compacted and cemented sediments?", "Sedimentary rock", "Igneous rock", "Metamorphic rock", "Mantle rock only", "Compaction and cementation lithify sediment into sedimentary rock."),
        ("What is weathering?", "Breakdown of rock in place", "Transport of sediment only", "Melting of the core", "Formation of clouds only", "Weathering physically or chemically breaks down rock without requiring transport."),
        ("What instrument measures atmospheric pressure?", "Barometer", "Thermometer", "Anemometer", "Hygrometer", "A barometer measures atmospheric pressure."),
        ("What instrument measures wind speed?", "Anemometer", "Barometer", "Rain gauge", "Seismometer", "An anemometer measures wind speed."),
        ("What instrument records earthquake ground motion?", "Seismometer", "Altimeter", "Calorimeter", "Spectrometer only", "A seismometer detects and records ground motion."),
        ("Which atmospheric layer contains most weather?", "Troposphere", "Stratosphere", "Mesosphere", "Thermosphere", "Most clouds and weather occur in the lowest layer, the troposphere."),
        ("Which energy input powers most global atmospheric circulation?", "Solar radiation", "Earth's magnetic field", "Moonlight", "Radioactive carbon", "Uneven solar heating drives pressure differences and atmospheric motion."),
        ("Which process moves water vapor from plant leaves into the atmosphere?", "Transpiration", "Infiltration", "Precipitation", "Condensation", "Plants release water vapor through stomata by transpiration."),
        ("What is an underground layer that stores and transmits groundwater called?", "Aquifer", "Watershed", "Glacier", "Delta", "An aquifer is permeable material that stores and transmits groundwater."),
        ("Which gas is most abundant in Earth's atmosphere?", "Nitrogen", "Oxygen", "Carbon dioxide", "Argon plus oxygen", "Nitrogen makes up about 78% of Earth's atmosphere."),
        ("Which planet is famous for the Great Red Spot?", "Jupiter", "Mars", "Venus", "Saturn", "The Great Red Spot is a long-lived storm in Jupiter's atmosphere."),
        ("Which planet rotates on its side with an axial tilt near 98 degrees?", "Uranus", "Mercury", "Earth", "Mars", "Uranus has an extreme axial tilt of about 98 degrees."),
        ("Which planet has the shortest orbital period around the Sun?", "Mercury", "Venus", "Mars", "Jupiter", "Mercury completes an orbit in about 88 Earth days."),
        ("What is the name of Earth's natural satellite?", "The Moon", "Phobos", "Titan", "Europa", "The Moon is Earth's only natural satellite."),
        ("What kind of object is the Sun?", "Star", "Planet", "Galaxy", "Comet", "The Sun is a main-sequence star."),
        ("What is a galaxy?", "A gravitationally bound system of stars, gas, and dust", "A single orbiting planet", "A cloud inside Earth's atmosphere", "A type of moon", "Galaxies are vast gravitationally bound systems containing stars and interstellar matter."),
        ("What causes the phases of the Moon?", "Changing view of its sunlit half", "Earth's shadow every week", "Changes in the Moon's own light output", "Clouds in Earth's atmosphere", "As the Moon orbits Earth, we see different portions of its illuminated half."),
        ("What is a light-year a unit of?", "Distance", "Time", "Brightness", "Mass", "A light-year is the distance light travels in one year."),
        ("Which object is the remnant core left by many low-mass stars?", "White dwarf", "Gas giant", "Asteroid belt", "Protostar", "Many low-mass stars end by leaving a dense white-dwarf core."),
        ("What is the path of one object around another called?", "Orbit", "Axis", "Spectrum", "Crater", "An orbit is the gravitationally governed path of one body around another."),
        ("Which observation provides direct evidence that Earth rotates?", "Foucault pendulum motion", "Changing Moon phases", "Ocean salinity", "Rock weathering", "The rotation of a Foucault pendulum's swing plane relative to the ground demonstrates Earth's rotation."),
        ("Which process in the Sun releases energy by combining light nuclei?", "Nuclear fusion", "Nuclear fission", "Combustion", "Chemical oxidation", "The Sun's energy comes mainly from fusion of hydrogen nuclei into helium."),
        ("Which vitamin can human skin synthesize with sufficient ultraviolet exposure?", "Vitamin D", "Vitamin C", "Vitamin B12", "Vitamin K only from blood", "Ultraviolet B exposure supports vitamin D synthesis in skin."),
        ("Which gas law relates pressure and volume at constant temperature?", "Boyle's law", "Charles's law", "Ohm's law", "Hooke's law", "Boyle's law states that pressure and volume vary inversely at constant temperature."),
        ("What is the boundary around a black hole beyond which light cannot escape called?", "Event horizon", "Photosphere", "Asteroid belt", "Magnetopause", "The event horizon is the causal boundary from within which escape is impossible."),
    ]

    return [
        item(*row)
        for row in rows
    ]


def build_medium_items() -> list[Item]:
    items: list[Item] = []

    density_cases = [
        ("a metal sample", 54, 6, "9 g/cm³", "324 g/cm³", "8 g/cm³", "60 g/cm³"),
        ("a mineral", 84, 12, "7 g/cm³", "1/7 g/cm³", "72 g/cm³", "96 g/cm³"),
        ("a liquid", 45, 50, "0.9 g/mL", "5 g/mL", "1.1 g/mL", "95 g/mL"),
        ("a plastic block", 72, 80, "0.9 g/cm³", "8 g/cm³", "1.25 g/cm³", "152 g/cm³"),
        ("a rock", 150, 60, "2.5 g/cm³", "90 g/cm³", "0.4 g/cm³", "210 g/cm³"),
    ]
    for subject, mass, volume, correct, wrong, d1, d2 in density_cases:
        items.append(item(
            f"What is the density of {subject} with mass {mass} grams and volume {volume} cubic centimeters?",
            correct, wrong, d1, d2,
            f"Density is mass divided by volume: {mass} ÷ {volume} = {correct.split()[0]}.",
        ))

    speed_cases = [
        ("a wave", 24, 6, "4 m/s", "144 m/s", "18 m/s", "30 m/s"),
        ("a pulse", 45, 9, "5 m/s", "405 m/s", "4 m/s", "54 m/s"),
        ("sound in a model", 80, 10, "8 m/s", "800 m/s", "70 m/s", "9 m/s"),
        ("a ripple", 36, 4, "9 m/s", "144 m/s", "8 m/s", "40 m/s"),
        ("a disturbance", 63, 7, "9 m/s", "441 m/s", "8 m/s", "70 m/s"),
    ]
    for subject, distance, time, correct, wrong, d1, d2 in speed_cases:
        items.append(item(
            f"{subject.capitalize()} travels {distance} meters in {time} seconds. What is its average speed?",
            correct, wrong, d1, d2,
            f"Average speed is distance divided by time: {distance} ÷ {time} = {correct}.",
        ))

    force_cases = [
        (4, 3, "12 N", "7 N", "1.33 N", "24 N"),
        (6, 5, "30 N", "11 N", "1.2 N", "60 N"),
        (2.5, 8, "20 N", "10.5 N", "3.2 N", "40 N"),
        (10, 1.5, "15 N", "11.5 N", "6.67 N", "150 N"),
        (7, 4, "28 N", "11 N", "1.75 N", "56 N"),
    ]
    for mass, acceleration, correct, wrong, d1, d2 in force_cases:
        items.append(item(
            f"What net force accelerates a {mass}-kilogram object at {acceleration} meters per second squared?",
            correct, wrong, d1, d2,
            f"Newton's second law gives F = ma = {mass} × {acceleration} = {correct}.",
        ))

    work_cases = [
        (20, 5, "100 J", "25 J", "4 J", "200 J"),
        (15, 8, "120 J", "23 J", "1.875 J", "60 J"),
        (50, 3, "150 J", "53 J", "16.7 J", "300 J"),
        (12, 9, "108 J", "21 J", "1.33 J", "216 J"),
        (40, 2.5, "100 J", "42.5 J", "16 J", "80 J"),
    ]
    for force, distance, correct, wrong, d1, d2 in work_cases:
        items.append(item(
            f"A constant force of {force} newtons moves an object {distance} meters in the force's direction. How much work is done?",
            correct, wrong, d1, d2,
            f"Work is force times parallel displacement: {force} × {distance} = {correct}.",
        ))

    power_cases = [
        (600, 3, "200 W", "1,800 W", "603 W", "197 W"),
        (900, 6, "150 W", "5,400 W", "906 W", "894 W"),
        (480, 4, "120 W", "1,920 W", "484 W", "476 W"),
        (750, 5, "150 W", "3,750 W", "755 W", "745 W"),
        (360, 2, "180 W", "720 W", "362 W", "358 W"),
    ]
    for energy, time, correct, wrong, d1, d2 in power_cases:
        items.append(item(
            f"A device transfers {energy} joules in {time} seconds. What is its average power?",
            correct, wrong, d1, d2,
            f"Power is energy divided by time: {energy} ÷ {time} = {correct}.",
        ))

    current_cases = [
        (12, 4, "3 A", "48 A", "8 A", "16 A"),
        (18, 6, "3 A", "108 A", "12 A", "24 A"),
        (20, 5, "4 A", "100 A", "15 A", "25 A"),
        (9, 3, "3 A", "27 A", "6 A", "12 A"),
        (24, 8, "3 A", "192 A", "16 A", "32 A"),
    ]
    for voltage, resistance, correct, wrong, d1, d2 in current_cases:
        items.append(item(
            f"A resistor has {voltage} volts across it and resistance {resistance} ohms. What current flows through it?",
            correct, wrong, d1, d2,
            f"Ohm's law gives I = V/R = {voltage}/{resistance} = {correct}.",
        ))

    wave_cases = [
        (2, 6, "12 m/s", "3 m/s", "8 m/s", "4 m/s"),
        (3, 5, "15 m/s", "1.67 m/s", "8 m/s", "30 m/s"),
        (4, 2.5, "10 m/s", "1.6 m/s", "6.5 m/s", "20 m/s"),
        (1.5, 8, "12 m/s", "5.33 m/s", "9.5 m/s", "6 m/s"),
        (0.5, 20, "10 m/s", "40 m/s", "20.5 m/s", "5 m/s"),
    ]
    for wavelength, frequency, correct, wrong, d1, d2 in wave_cases:
        items.append(item(
            f"A wave has wavelength {wavelength} meters and frequency {frequency} hertz. What is its speed?",
            correct, wrong, d1, d2,
            f"Wave speed is wavelength times frequency: {wavelength} × {frequency} = {correct}.",
        ))

    items.extend([
        item("A plant is placed in darkness for several days. Which process directly decreases first?", "Light-dependent photosynthetic reactions", "Cellular respiration stops completely", "DNA replication in every cell", "Water absorption becomes impossible", "Light-dependent reactions require light and therefore fall directly when light is removed."),
        item("Why do root hair cells have long projections?", "To increase surface area for water and mineral uptake", "To produce seeds", "To pump blood", "To reduce contact with soil", "Long projections increase contact area with soil solution."),
        item("A population has abundant food but no nesting sites. What is the nesting-site availability?", "A limiting factor", "A producer", "A mutation rate", "An abiotic energy source only", "A scarce required resource limits population growth."),
        item("Why can antibiotics fail against viruses?", "Viruses lack the bacterial structures and processes targeted by antibiotics", "Viruses are always larger than bacteria", "Antibiotics only work below freezing", "Viruses contain no genetic material", "Antibiotics target bacterial machinery that viruses do not possess."),
        item("Why does sweating cool the body?", "Higher-energy water molecules evaporate and carry energy away", "Sweat freezes on the skin", "Sweat stops all blood flow", "Water creates new cold energy", "Evaporation removes thermal energy from the skin."),
        item("Why can vaccination produce faster later immune responses?", "It creates memory cells specific to the antigen", "It permanently raises body temperature", "It removes every pathogen from the environment", "It replaces red blood cells", "Memory lymphocytes respond rapidly upon later exposure."),
        item("A heterozygous organism has which allele arrangement for one gene?", "Two different alleles", "Two identical dominant alleles only", "No alleles", "Four identical chromosomes", "Heterozygous means carrying two different alleles at a locus."),
        item("Which event increases genetic variation during meiosis?", "Crossing over between homologous chromosomes", "Copying every chromosome without division", "Mitosis of skin cells", "Translation at ribosomes", "Crossing over creates new allele combinations."),
        item("What happens to enzyme activity when temperature rises far above the enzyme's optimum?", "It usually decreases as the enzyme denatures", "It increases without limit", "It becomes independent of shape", "The enzyme becomes DNA", "High temperature can disrupt the enzyme's three-dimensional active site."),
        item("Why are decomposers important to ecosystems?", "They return nutrients from dead material to the environment", "They create sunlight", "They eliminate all consumers", "They prevent any respiration", "Decomposition recycles matter into forms available to other organisms."),
        item("Which observation best indicates that a chemical reaction occurred?", "A new substance with new properties formed", "A solid was cut into smaller pieces", "Water changed containers", "A metal was polished", "Formation of new substances defines chemical change."),
        item("Why does increasing reactant concentration often increase reaction rate?", "Particles collide more frequently", "Every particle gains infinite energy", "Activation energy becomes mass", "Products turn back into elements", "More particles per volume generally produce more collision opportunities."),
        item("What happens to equilibrium when more reactant is added to a reversible reaction at equilibrium?", "The system shifts toward consuming some added reactant", "All reactions stop permanently", "The equilibrium constant becomes zero at fixed temperature", "Mass is destroyed", "Le Châtelier's principle predicts a shift opposing the concentration increase."),
        item("Why does table salt conduct electricity when molten but not as a solid?", "Its ions can move when molten but are fixed in the solid lattice", "Its atoms disappear when solid", "Molten salt contains free protons only", "Solid salt has no charged particles", "Mobile ions carry current in the molten state."),
        item("Why does crushing a solid reactant often speed its reaction?", "It increases exposed surface area", "It reduces the number of particles to zero", "It changes every atom's identity", "It always lowers temperature", "Greater surface area allows more particle collisions at the interface."),
        item("In an exothermic reaction, how does chemical energy of products compare with reactants?", "Products have lower chemical energy", "Products always have greater mass", "Products have identical energy in every reaction", "Reactants contain no energy", "Exothermic reactions release energy, leaving products at lower chemical energy."),
        item("Which separation method is best for obtaining pure water from saltwater?", "Distillation", "Filtration alone", "Magnetic separation", "Chromatography of solids only", "Distillation vaporizes and condenses water while leaving dissolved salt behind."),
        item("Why does an ionic compound usually have a high melting point?", "Strong electrostatic attractions hold its ions in a lattice", "Its molecules have no forces", "All ionic compounds are gases", "Its electrons have no charge", "Substantial energy is needed to overcome lattice attractions."),
        item("An ion has 17 protons and a net charge of 1-. How many electrons does it have?", "18", "16", "17", "34", "One extra negative charge means one more electron than proton, so it has 18 electrons."),
        item("Two atoms have the same proton number but different neutron numbers. What are they?", "Isotopes of the same element", "Different elements necessarily", "Identical ions only", "Molecules", "Element identity depends on proton number; neutron variation produces isotopes."),
        item("A moving cart's speed doubles while its mass stays constant. How does its kinetic energy change?", "It becomes four times as large", "It doubles", "It halves", "It stays unchanged", "Kinetic energy is proportional to speed squared."),
        item("Why does a passenger move forward when a stopping bus brakes suddenly?", "Inertia tends to maintain the passenger's forward motion", "Gravity reverses direction", "The passenger loses all mass", "Air pressure becomes zero", "Newton's first law describes resistance to a change in motion."),
        item("A floating object displaces water weighing 12 newtons. What is the buoyant force on it?", "12 newtons upward", "12 newtons downward", "Zero", "24 newtons upward", "For floating equilibrium, buoyant force equals the displaced fluid's weight."),
        item("Why is pressure greater at greater depth in a stationary liquid?", "More fluid weight lies above each unit area", "Liquid density always becomes zero", "Gravity stops at the surface", "Depth removes molecules", "Hydrostatic pressure increases with the weight of overlying fluid."),
        item("Which energy change occurs as a ball falls freely without air resistance?", "Gravitational potential energy becomes kinetic energy", "Kinetic energy becomes mass", "Chemical energy becomes nuclear energy", "Total mechanical energy disappears", "Mechanical energy is conserved while potential energy converts to kinetic energy."),
        item("Why can a convex lens form a real image?", "It can converge rays so they actually meet", "It reflects all light backward", "It blocks every ray", "It always makes parallel rays diverge", "A converging lens can bring refracted rays to a physical focus."),
        item("When a wave enters a slower medium at an angle, why does it refract?", "One side of the wavefront changes speed first", "Its frequency becomes infinite", "Its energy changes into matter", "The boundary removes all wavelength", "A speed change across the wavefront changes its direction."),
        item("Why are household appliances connected in parallel?", "Each receives the full supply voltage and can operate independently", "The same current must pass through every appliance", "Opening one switch must stop all appliances", "Parallel wiring eliminates resistance", "Parallel branches share voltage and remain independently switchable."),
        item("What happens to total resistance when another resistor is added in parallel?", "It decreases", "It always doubles", "It becomes the sum of all resistances", "It becomes infinite", "An added parallel path increases conductance and lowers equivalent resistance."),
        item("What does the area under a velocity-time graph represent?", "Displacement", "Acceleration only", "Mass", "Power", "Integrating velocity over time gives displacement."),
        item("Which plate-boundary process commonly creates a deep-ocean trench?", "Subduction", "Transform sliding only", "Continental rifting only", "Weathering", "A descending plate bends at a subduction zone and forms a trench."),
        item("Why are volcanic arcs often found above subduction zones?", "Water from the descending slab promotes mantle melting", "The slab freezes the entire mantle", "Ocean tides create magma directly", "Earth's core reaches the surface", "Fluids from the slab lower melting temperatures in the overlying mantle."),
        item("What weather is commonly associated with a cold front passing?", "A narrow band of rising air and possible heavy showers", "Weeks of completely unchanged air", "No wind or cloud under any conditions", "Permanent warming everywhere", "Dense cold air lifts warm air rapidly along a cold front."),
        item("Why do coastal areas often have smaller daily temperature ranges than inland areas?", "Water heats and cools more slowly than land", "Ocean water has no heat capacity", "Coasts receive no sunlight", "Land cannot store thermal energy", "Water's high heat capacity moderates nearby air temperatures."),
        item("What happens to rising unsaturated air as atmospheric pressure decreases?", "It expands and cools", "It compresses and warms", "It becomes denser without changing temperature", "It loses all molecules", "Lower surrounding pressure lets rising air expand, doing work and cooling."),
        item("Why is the leeward side of a mountain often drier?", "Descending air warms and its relative humidity falls", "All clouds move underground", "The Sun stops shining there", "Air loses nitrogen on the windward side", "After moisture loss aloft, descending leeward air warms and becomes relatively dry."),
        item("Which process turns loose sediment into sedimentary rock?", "Compaction and cementation", "Melting and crystallization", "Nuclear fusion", "Evaporation only", "Burial compacts sediment and minerals cement grains together."),
        item("Why do seasons occur on Earth?", "Earth's tilted axis changes solar angle and day length during its orbit", "Earth moves much closer to the Sun every summer everywhere", "The Sun changes temperature each month", "The Moon blocks sunlight seasonally", "Axial tilt produces seasonal changes in illumination."),
        item("Why do we always see nearly the same face of the Moon?", "Its rotation period equals its orbital period around Earth", "The Moon does not rotate", "Earth's shadow hides its far side", "The far side emits no light", "Synchronous rotation keeps one lunar hemisphere facing Earth."),
        item("What causes a solar eclipse?", "The Moon passes between Earth and the Sun", "Earth passes between the Sun and Moon", "The Sun passes behind Mars", "Clouds cover the entire Sun globally", "A solar eclipse occurs when the Moon blocks sunlight from reaching part of Earth."),
        item("Why are spectral lines useful to astronomers?", "They reveal chemical elements that absorb or emit particular wavelengths", "They directly measure an object's mass without assumptions", "They make gravity disappear", "They show only the object's shape", "Atoms and ions have characteristic spectral transitions."),
        item("What supports the conclusion that the universe is expanding?", "Most distant galaxies show redshift increasing with distance", "All stars have identical brightness", "The Moon has phases", "Earth has seasons", "Cosmological redshift and the distance-redshift relation indicate expansion."),
        item("Why is a control group used in an experiment?", "To provide a baseline for comparison", "To guarantee the hypothesis is true", "To change every variable at once", "To remove the need for measurements", "A control group helps isolate the effect of the independent variable."),
        item("Which variable is deliberately changed by an experimenter?", "Independent variable", "Dependent variable", "Controlled conclusion", "Random error", "The independent variable is manipulated to test its effect."),
        item("Which variable is measured as the outcome of an experiment?", "Dependent variable", "Independent variable", "Control constant only", "Sample label", "The dependent variable is the measured response."),
        item("Why are repeated trials useful?", "They reduce the influence of random variation", "They eliminate every systematic error automatically", "They prove causation without controls", "They make sample size smaller", "Replication improves precision and reveals random variability."),
        item("A measurement is close to the accepted value but repeated measurements vary widely. How is it described?", "Accurate but imprecise", "Precise but inaccurate", "Both perfectly accurate and precise", "Neither measurable nor testable", "Closeness to the accepted value is accuracy; wide spread indicates low precision."),
        item("What does a scientific model do?", "Represents selected features of a system for explanation or prediction", "Duplicates reality in every detail", "Replaces all observations", "Guarantees a theory can never change", "Models simplify systems while retaining relevant relationships."),
        item("Why should only one main factor be changed in a controlled experiment?", "To attribute outcome differences to that factor", "To maximize confounding", "To ensure no data are collected", "To make controls unnecessary", "Holding other factors constant supports causal interpretation."),
        item("What does a larger sample size generally improve?", "Reliability of an estimated population pattern", "The certainty that bias is absent", "The value of every individual measurement", "The ability to ignore sampling design", "Larger representative samples reduce random sampling uncertainty."),
        item("A graph shows plant height rising as fertilizer increases, then falling at the highest dose. What is the best conclusion?", "There is an intermediate fertilizer level associated with greatest height", "More fertilizer always increases height", "Fertilizer has no relationship to height", "The highest dose caused infinite growth", "The observed peak indicates a nonmonotonic response with an intermediate optimum."),
        item("Why must units accompany most quantitative scientific measurements?", "They define the scale and kind of quantity", "They change the measured object", "They remove all uncertainty", "They make arithmetic optional", "A numerical value without its unit is often ambiguous."),
        item("Which graph is usually appropriate for change in temperature over continuous time?", "Line graph", "Unordered pie chart", "Single photograph only", "Taxonomic tree", "A line graph displays a continuous variable changing over ordered time."),
        item("Why is correlation alone insufficient to establish causation?", "A third factor or reverse influence may explain the association", "Correlated variables can never be related", "Causation requires identical values", "All correlations are measurement errors", "Association does not by itself rule out confounding or reverse causality."),
        item("A balance consistently reads 2 grams too high. What kind of error is this?", "Systematic error", "Random error only", "Sampling variation", "Biological mutation", "A consistent offset is a systematic measurement bias."),
        item("What is peer review intended to assess before publication?", "Whether methods, reasoning, and evidence meet disciplinary standards", "Whether results support a preferred answer", "Whether no uncertainty exists", "Whether experiments need not be repeatable", "Peer reviewers evaluate the rigor and clarity of submitted work."),
        item("Why do alveoli have very thin walls?", "To shorten the diffusion distance for respiratory gases", "To store solid food", "To prevent any blood flow", "To produce bone tissue", "Thin alveolar and capillary walls allow rapid oxygen and carbon-dioxide diffusion."),
        item("Why does heart rate usually rise during vigorous exercise?", "Working muscles require faster oxygen delivery and waste removal", "Blood no longer contains water", "The lungs stop exchanging gases", "All cells stop respiring", "Higher cardiac output supports increased muscle metabolism."),
        item("What happens to a red blood cell placed in a strongly hypotonic solution?", "Water enters and the cell may burst", "Water leaves and the cell shrinks", "No water can cross its membrane", "The cell becomes a bacterium", "Osmosis moves water into the cell from the lower-solute solution."),
        item("Why can a recessive allele remain in a population without appearing in every carrier?", "A dominant allele can mask it in heterozygotes", "Recessive alleles contain no DNA", "Carriers have no chromosomes", "Every recessive allele is immediately removed", "A heterozygote can carry a recessive allele while showing the dominant phenotype."),
        item("A plant bends toward a window. Which response is this?", "Positive phototropism", "Negative gravitropism", "Random mutation", "Transpiration only", "Growth toward light is positive phototropism."),
        item("Why does soap help remove grease with water?", "Its molecules interact with both nonpolar grease and polar water", "It converts grease into an element", "It makes water nonmolecular", "It eliminates surface area", "Amphiphilic soap molecules form structures that disperse grease in water."),
        item("A gas is compressed at constant temperature. According to Boyle's law, what happens to its pressure?", "It increases", "It decreases to zero", "It remains unchanged", "It becomes negative", "At constant temperature pressure is inversely proportional to volume."),
        item("Why does increasing temperature usually increase gas pressure in a sealed rigid container?", "Particles collide with the walls more forcefully and frequently", "The container loses all particles", "Particle motion stops", "The gas becomes a vacuum", "Higher temperature raises average molecular kinetic energy."),
        item("What occurs at the cathode during electrolysis?", "Reduction", "Oxidation", "Combustion", "Neutralization only", "Reduction, or gain of electrons, occurs at the cathode."),
        item("Why does graphite conduct electricity while diamond does not conduct well?", "Graphite has delocalized electrons that can move between layers", "Diamond contains no carbon", "Graphite is always molten", "Diamond has free ions in solution", "Graphite's bonding leaves mobile delocalized electrons."),
        item("A 5-kilogram object is lifted 4 meters near Earth using g = 10 m/s². How much gravitational potential energy is gained?", "200 J", "20 J", "50 J", "2,000 J", "The gain is mgh = 5×10×4 = 200 joules."),
        item("A car changes velocity from 5 m/s to 17 m/s in 4 seconds. What is its average acceleration?", "3 m/s²", "5.5 m/s²", "12 m/s²", "48 m/s²", "Acceleration is change in velocity divided by time: (17-5)/4 = 3 m/s²."),
        item("A wave's speed stays constant while its frequency doubles. What happens to its wavelength?", "It halves", "It doubles", "It stays unchanged", "It becomes four times as large", "From v = fλ, fixed speed means wavelength is inversely proportional to frequency."),
        item("Why is wood often used for a saucepan handle?", "Its low thermal conductivity slows heat transfer to the hand", "It is always colder than its surroundings", "It creates cold energy", "It contains no vibrating particles", "Wood is a thermal insulator compared with metal."),
        item("Which change increases the turning effect of a fixed force on a lever?", "Applying it farther from the pivot", "Applying it at the pivot", "Shortening the perpendicular distance", "Removing the force", "Torque equals force times perpendicular distance from the pivot."),
        item("Why are S-waves absent from seismic records beyond Earth's liquid outer core?", "Shear waves cannot propagate through liquids", "S-waves travel only through air", "The mantle absorbs all waves", "The core contains no matter", "Liquids do not support the shear restoring force required by S-waves."),
        item("What is the likely result when moist air is forced upward over a mountain?", "It cools, may condense, and can produce precipitation", "It always warms and dries immediately", "Its pressure rises without compression", "All water vapor disappears chemically", "Rising air expands and cools, promoting saturation and condensation."),
        item("Why does the apparent position of nearby stars shift against distant stars over six months?", "Earth views them from different points in its orbit", "The stars reverse their own rotation", "The Moon changes their color", "Earth's atmosphere stops refracting light", "The baseline across Earth's orbit produces annual stellar parallax."),
        item("A radioactive sample falls from 800 counts per minute to 200 counts per minute in two half-lives. What fraction remains?", "1/4", "1/2", "3/4", "1/8", "Two halvings leave (1/2)² = 1/4 of the original activity."),
    ])

    if len(items) != 110:
        raise ValueError(
            f"Expected 110 medium science items, found {len(items)}"
        )

    return items


def build_hard_items() -> list[Item]:
    return [
        item("A plant species has allele T dominant over t. What fraction of offspring from Tt × Tt are expected to show the recessive phenotype?", "1/4", "1/2", "3/4", "0", "The genotype ratio is 1 TT : 2 Tt : 1 tt, and only tt is recessive."),
        item("Two unaffected parents have a child with a rare recessive trait. Assuming simple Mendelian inheritance, what must be true of both parents?", "Both are carriers", "Both show the trait", "Neither has the allele", "Only the father carries the allele", "An affected child receives one recessive allele from each unaffected heterozygous parent."),
        item("A cell with 16 chromosomes undergoes meiosis. How many chromosomes should each normal gamete receive?", "8", "16", "32", "4", "Meiosis halves chromosome number from diploid 16 to haploid 8."),
        item("A DNA template triplet changes but the encoded amino acid stays the same. What kind of coding outcome is this?", "Silent mutation", "Frameshift mutation", "Nonsense mutation necessarily", "Chromosome duplication", "Redundancy in the genetic code can let a base substitution preserve the amino acid."),
        item("In a dihybrid cross AaBb × AaBb with independent assortment, what fraction is expected to show both recessive traits?", "1/16", "1/4", "3/16", "9/16", "Each recessive phenotype has probability 1/4, and independence gives 1/4 × 1/4 = 1/16."),
        item("A food chain transfers about 10% of energy between trophic levels. If producers contain 50,000 kJ, about how much reaches secondary consumers?", "500 kJ", "5,000 kJ", "50 kJ", "45,000 kJ", "Primary consumers receive about 5,000 kJ and secondary consumers about 500 kJ."),
        item("A population grows rapidly and then levels near a stable size. Which model best describes this pattern?", "Logistic growth approaching carrying capacity", "Unlimited exponential growth", "Linear decay to zero", "Random mutation only", "Resource limitation causes logistic growth to slow near carrying capacity."),
        item("An inhibitor binds away from an enzyme's active site and changes its shape. What type of inhibition is most consistent?", "Noncompetitive inhibition", "Competitive inhibition", "Substrate activation", "DNA replication", "Binding at an allosteric site is characteristic of noncompetitive inhibition."),
        item("A sealed ecosystem receives light but exchanges no matter with its surroundings. Which process must balance respiration over the long term?", "Photosynthesis", "Predation", "Mutation", "Evaporation alone", "Photosynthesis must replace organic matter and oxygen consumed by respiration."),
        item("A 10-gram sample of calcium carbonate decomposes completely in a closed vessel. What must be true of the total product mass?", "It is 10 grams", "It is less than 10 grams", "It is greater than 10 grams", "It is zero", "Conservation of mass requires total product mass to equal reactant mass in the closed vessel."),
        item("For 2H2 + O2 → 2H2O, how many moles of water can form from 3 moles of O2 with excess hydrogen?", "6 moles", "3 moles", "1.5 moles", "9 moles", "The equation forms 2 moles of water per mole of oxygen, so 3 moles O2 yields 6 moles water."),
        item("A reaction rate doubles when reactant concentration doubles while other conditions remain fixed. What reaction order with respect to that reactant is consistent?", "First order", "Zero order", "Second order necessarily", "Negative first order", "For first-order dependence, doubling concentration doubles rate."),
        item("A buffer contains a weak acid and its conjugate base. Why does it resist a small added amount of strong acid?", "The conjugate base consumes much of the added hydrogen ions", "The buffer prevents any ions from forming", "The weak acid becomes a metal", "The solution's volume becomes zero", "The conjugate base neutralizes added acid, limiting the pH change."),
        item("Two identical bulbs are connected in series to an ideal battery. If one bulb's filament breaks, what happens to the other?", "It goes out because the circuit opens", "It becomes twice as bright", "It remains unchanged", "It receives infinite current", "A break anywhere in a series circuit interrupts current through the entire loop."),
        item("Two resistors of 6 ohms and 3 ohms are connected in parallel. What is their equivalent resistance?", "2 ohms", "9 ohms", "4.5 ohms", "3 ohms", "For parallel resistors, 1/R = 1/6 + 1/3 = 1/2, so R = 2 ohms."),
        item("A 2-kilogram object moving at 6 m/s stops uniformly in 3 seconds. What is the magnitude of the average net force?", "4 N", "12 N", "1 N", "36 N", "Acceleration magnitude is 6/3 = 2 m/s², so force magnitude is 2×2 = 4 N."),
        item("A projectile is launched horizontally in ideal conditions. Which statement compares its horizontal and vertical motions?", "Horizontal velocity is constant while vertical velocity changes due to gravity", "Both velocities remain zero", "Horizontal acceleration equals gravity", "Vertical velocity is constant", "With no air resistance, gravity affects only the vertical component."),
        item("A motor draws 200 watts and provides 150 watts of mechanical output. What is its efficiency?", "75%", "133%", "50%", "25%", "Efficiency is useful output divided by input: 150/200 = 75%."),
        item("Air at 20 degrees Celsius holds half the water vapor required for saturation at that temperature. What is its relative humidity?", "50%", "20%", "100%", "2%", "Relative humidity is actual vapor amount divided by saturation amount, here one half."),
        item("At a transform plate boundary, what geological hazard is most directly expected?", "Shallow earthquakes", "A volcanic island arc necessarily", "A deep-ocean trench necessarily", "No crustal stress", "Transform motion builds and releases shear stress, producing shallow earthquakes."),
        item("A star has the same surface temperature as the Sun but four times the radius. How does its luminosity compare, assuming blackbody behavior?", "It is 16 times as luminous", "It is 4 times as luminous", "It has the same luminosity", "It is 8 times as luminous", "At fixed temperature luminosity is proportional to surface area, hence radius squared."),
        item("A planet orbits the same star at four times another planet's orbital radius. Using Kepler's third law, how does its orbital period compare?", "It is 8 times as long", "It is 4 times as long", "It is 16 times as long", "It is 2 times as long", "Period scales as orbital radius to the 3/2 power, and 4^(3/2) = 8."),
    ]


def build_science_items() -> dict[str, list[Item]]:
    easy = build_easy_items()
    medium = build_medium_items()
    hard = build_hard_items()

    if len(easy) != 88:
        raise ValueError(
            f"Expected 88 easy science items, found {len(easy)}"
        )

    if len(hard) != 22:
        raise ValueError(
            f"Expected 22 hard science items, found {len(hard)}"
        )

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }
