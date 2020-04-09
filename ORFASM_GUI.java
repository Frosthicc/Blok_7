import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * ORFASM_GUI is an application used for visualisation of ORFS, and parsing them to other methods.
 * This class is the main director of this application, calling multiple java and python methods.
 * These methods can be called from withing a GUI.
 *
 * @author Bart Jolink
 */
public class ORFASM_GUI extends JFrame implements ActionListener {


    private static String py_outputfile, header, sequence, orf_seq;
    private static JButton button1, button2, button3, button4, button5, button6, emptybutton1, emptybutton2;
    private static JTextField text1, text3;
    private static JTextArea text2;
    private static JLabel label1, label2, label3, label4, emptylabel, labelinfo1, labelinfo2;
    private static JPanel panel1, panel2;
    private static JCheckBox boxes[];
    private static JScrollPane scroller;
    private static String[] orfArray, startposArray, endposArray;

    /**
     * Main function, used to call GUI and build frame
     */
    public static void main(String[] args) {
        ORFASM_GUI frame = new ORFASM_GUI();
        frame.setSize(650, 550);
        frame.createGUI();
        frame.setVisible(true);
        frame.setTitle("ORFASM ©Bart Jolink, Paul Verhoeven - 2020");

    }

    /**
     * This method builds the GUI with all its elements.
     */
    private void createGUI() {
        // Creating window layout.
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        Container window = getContentPane();
        window.setLayout(new GridBagLayout());
        window.setBackground(Color.lightGray);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.weightx = 1;
        ;
        gbc.weighty = 1;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.insets = new Insets(5, 5, 5, 5);

        // Creating buttons, textareas, labels and panels below.
        button1 = new JButton("Choose file");
        button1.setFont(new Font("Arial", Font.BOLD, 13));
        button1.setBorderPainted(false);
        button1.setBackground(Color.pink);
        button1.addActionListener(new ChooseFile());
        gbc.gridx = 4;
        gbc.gridy = 9;
        gbc.gridwidth = 1;
        window.add(button1, gbc);

        button2 = new JButton("Find ORFs");
        button2.setFont(new Font("Arial", Font.BOLD, 13));
        button2.setBackground(Color.pink);
        button2.setBorderPainted(false);
        button2.addActionListener(new DisplayORFS());
        gbc.gridx = 1;
        gbc.gridy = 7;
        gbc.gridwidth = 1;
        window.add(button2, gbc);

        button3 = new JButton("Save ORFs in database");
        button3.setFont(new Font("Arial", Font.BOLD, 13));
        button3.setBackground(Color.pink);
        button3.setBorderPainted(false);
        button3.addActionListener(new SaveORFS());
        gbc.gridx = 2;
        gbc.gridy = 7;
        gbc.gridwidth = 1;
        window.add(button3, gbc);

        button4 = new JButton("Blast selected ORFs");
        button4.setFont(new Font("Arial", Font.BOLD, 13));
        button4.setBackground(Color.pink);
        button4.setBorderPainted(false);
        button4.addActionListener(new BlastORFS());
        gbc.gridx = 3;
        gbc.gridy = 7;
        gbc.gridwidth = 1;
        window.add(button4, gbc);

        button5 = new JButton("Select all ORFs");
        button5.setFont(new Font("Arial", Font.BOLD, 13));
        button5.setBackground(Color.GRAY);
        button5.setBorderPainted(false);
        button5.addActionListener(new CheckAllAction());
        gbc.gridx = 4;
        gbc.gridy = 1;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        window.add(button5, gbc);

        button6 = new JButton("De-select all ORFs");
        button6.setFont(new Font("Arial", Font.BOLD, 13));
        button6.setBackground(Color.GRAY);
        button6.setBorderPainted(false);
        button6.addActionListener(new UnCheckAllAction());
        gbc.gridx = 4;
        gbc.gridy = 2;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        window.add(button6, gbc);

        emptybutton1 = new JButton();
        emptybutton1.setContentAreaFilled(false);
        emptybutton1.setBorderPainted(false);
        gbc.gridx = 4;
        gbc.gridy = 3;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        window.add(emptybutton1, gbc);

        emptybutton2 = new JButton();
        emptybutton2.setContentAreaFilled(false);
        emptybutton2.setBorderPainted(false);
        gbc.gridx = 4;
        gbc.gridy = 4;
        gbc.gridwidth = 1;
        gbc.gridheight = 1;
        window.add(emptybutton2, gbc);

        text1 = new JTextField(20);
        gbc.gridx = 1;
        gbc.gridy = 9;
        gbc.gridwidth = 3;
        gbc.gridheight = 1;
        window.add(text1, gbc);

        panel1 = new JPanel(new GridBagLayout());
        panel1.setPreferredSize(new Dimension(200, 400));
        panel1.setBackground(Color.lightGray);
        gbc.gridx = 1;
        gbc.gridy = 1;
        gbc.gridwidth = 3;
        gbc.gridheight = 5;
        panel2 = new JPanel(new GridBagLayout());
        panel2.setBackground(Color.white);
        scroller = new JScrollPane(panel2, ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS, ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        scroller.setBackground(Color.white);
        window.add(panel1, gbc);

        gbc.gridx = 1;
        gbc.gridy = 1;
        gbc.gridwidth = 3;
        gbc.gridheight = 1;
        panel1.add(scroller, gbc);
    }

    /**
     * This method gets ORFs from another python script which requires an .fa file as input.
     */
    private String[] getORFS(String file) throws IOException {
        String dir = System.getProperty("user.dir");
        py_outputfile = "placeholder.txt";
        Runtime rt = Runtime.getRuntime();
        try {
            String command_cd = String.format("cd %s", dir);
            String command_py = String.format("Orf_finder.exe %s %s", file, py_outputfile);
            String command = command_cd + " && " + command_py;
            System.out.println(command);
            Process python = new ProcessBuilder("cmd.exe", "/c", command).start();
            python.waitFor();
        } catch (IOException | InterruptedException e) {
        }
        System.out.println(dir + "\\" + py_outputfile);
        String data = new String(Files.readAllBytes(Paths.get(dir + "\\" + py_outputfile)));
        String[] dataArray = data.split("\n");
        header = dataArray[0];
        sequence = dataArray[1];
        orfArray = new String[dataArray.length - 2];
        startposArray = new String[dataArray.length - 2];
        endposArray = new String[dataArray.length - 2];
        for (int i = 2; i < dataArray.length - 1; i++) {
            System.out.println(dataArray[i - 2]);
            orfArray[i - 2] = dataArray[i].split("\t")[0];
            startposArray[i - 2] = dataArray[i].split("\t")[1];
            endposArray[i - 2] = dataArray[i].split("\t")[2];
        }
        System.out.println(orfArray);
        System.out.println(startposArray);
        System.out.println(endposArray);
        return orfArray;
    }

    /**
     * This method chooses a file sets the filepath in a textfield.
     */
    private class ChooseFile extends AbstractAction {
        // Selecting file to file and getting filePath

        @Override
        public void actionPerformed(ActionEvent e) {
            String filePath = "";
            JFileChooser fileChooser = new JFileChooser();
            int returnValue = fileChooser.showOpenDialog(null);
            if (returnValue == JFileChooser.APPROVE_OPTION) {
                File selectedFile = fileChooser.getSelectedFile();
                filePath = selectedFile.getPath();
                text1.setText(filePath);
            }
        }
    }

    /**
     * This method visualizes the ORFs as a checkbox.
     */
    private class DisplayORFS extends AbstractAction {

        @Override
        public void actionPerformed(ActionEvent button) {
            String file = text1.getText();
            if (file.isEmpty()) {
                // if no file is selected, give message.
                Graphics square = panel2.getGraphics();
                square.setFont(new Font("Arial", Font.BOLD, 40));
                square.drawString("NO FILE SELECTED", 30, 200);
            } else {
                try {
                    // try to get ORfs.
                    orfArray = getORFS(file);
                } catch (IOException e) {
                }
                // display checkbox for each ORF in array.
                boxes = new JCheckBox[orfArray.length];
                GridBagConstraints gbc = new GridBagConstraints();
                for (int i = 0; i < boxes.length; i++) {
                    boxes[i] = new JCheckBox(startposArray[i] + " " + endposArray[i] + " " + orfArray[i]);
                    boxes[i].setBackground(Color.white);
                    boxes[i].setBorderPainted(false);
                    gbc.insets = new Insets(1, 1, 1, 1);
                    gbc.anchor = GridBagConstraints.NORTHWEST;
                    gbc.gridy = i + 1;
                    gbc.gridx = 1;
                    panel2.add(boxes[i], gbc);
                    panel2.revalidate();
                }
            }
        }
    }

    /**
     * This method builds the GUI with all its elements.
     */
    private class SaveORFS extends AbstractAction {

        @Override
        public void actionPerformed(ActionEvent e) {
            // save information to be parsed in temporary file.
            PrintWriter writer = null;
            try {
                writer = new PrintWriter("temp.txt", StandardCharsets.UTF_8);
                writer.println(header);
                writer.println(sequence);
                for (JCheckBox box : boxes) {
                    if (box.isSelected()) {
                        writer.println(box.getText());
                        Runtime rt = Runtime.getRuntime();
                    }
                }
                writer.close();
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            try {
                // use ORF_parse_db.exe as executable to parse information to database.
                String dir = System.getProperty("user.dir");
                String command_cd = String.format("cd %s", dir);
                String command_py = "ORF_parse_db.exe \"orf_results\"";
                String command = command_cd + " && " + command_py;
                System.out.println(command);
                Process python = new ProcessBuilder("cmd.exe", "/c", command).start();
                python.waitFor();
                boolean f= new File("temp.txt").delete();
            } catch (IOException | InterruptedException ee) {
                ee.printStackTrace();
            }
        }
    }

    /**
     * This method gives ORFs to another python script which saves them in a database.
     */
    private class BlastORFS extends AbstractAction {

        @Override
        public void actionPerformed(ActionEvent ee) {
            // save information to be parsed in temporary file.
            PrintWriter writer = null;
            try {
                writer = new PrintWriter("temp.txt", StandardCharsets.UTF_8);
                writer.println(header);
                writer.println(sequence);
                for (JCheckBox box : boxes) {
                    if (box.isSelected()) {
                        writer.println(box.getText());
                        Runtime rt = Runtime.getRuntime();
                    }
                }
                writer.close();
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            try {
                // use ORF_blast.exe as executable to blast information and parse to database.
                String dir = System.getProperty("user.dir");
                String command_cd = String.format("cd %s", dir);
                String command_py = "ORF_blast.exe";
                String command = command_cd + " && " + command_py;
                System.out.println(command);

                ProcessBuilder pb = new ProcessBuilder("cmd.exe", "/c", command);
                pb.redirectErrorStream(true);
                Process python = pb.start();
                BufferedReader reader = new BufferedReader(new InputStreamReader(python.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null)
                    System.out.println("tasklist: " + line);
                python.waitFor();
                boolean f= new File("temp.txt").delete();
            } catch (IOException | InterruptedException eee) {
                eee.printStackTrace();
            }
        }
    }

    /**
     * This action is called when pressed the uncheck all button.
     * It un-checks all checkboxes
     */
    private class UnCheckAllAction extends AbstractAction {

        @Override
        public void actionPerformed(ActionEvent e) {

            for (int i = 0; i < boxes.length; i++) {
                boxes[i].setSelected(false);
            }
        }
    }

    /**
     * This action is called when pressed the check all button.
     * It checks all checkboxes
     */
    private class CheckAllAction extends AbstractAction {

        @Override
        public void actionPerformed(ActionEvent e) {

            for (int i = 0; i < boxes.length; i++) {
                boxes[i].setSelected(true);
            }
        }
    }

    @Override
    public void actionPerformed(ActionEvent button) {
    }
}
