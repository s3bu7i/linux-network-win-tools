package com.client;

import javax.swing.*;
import java.awt.*;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.Socket;

public class Client {
    private static DataOutputStream dataOutputStream = null;
    private static DataInputStream dataInputStream = null;
    private static String HOST= "localhost";
    private static Integer PORT= 5000;

    public static void main(String[] args) {
        while (true) {
            try {
                JFileChooser file = new JFileChooser() {
                    @Override
                    protected JDialog createDialog(Component parent) throws HeadlessException {
                        
                        JDialog dialog = super.createDialog(parent);
                        dialog.setModal(true);
                        dialog.setAlwaysOnTop(true);
                        return dialog;
                    }
                };
                file.setFileSelectionMode(JFileChooser.FILES_ONLY);

                int i = file.showSaveDialog(null);
                if (1 == i) {
                    System.out.println("No file selected");
                    break;
                } else {
                    Socket socket = new Socket(HOST,PORT);

                    dataInputStream = new DataInputStream(socket.getInputStream());
                    dataOutputStream = new DataOutputStream(socket.getOutputStream());

                    File arquivo = file.getSelectedFile();
                    sendFile(arquivo.getPath());
                    dataInputStream.close();
                    dataInputStream.close();
                    socket.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private static void sendFile(String path) throws Exception{
        int bytes = 0;
        File file = new File(path);
        FileInputStream fileInputStream = new FileInputStream(file);

        dataOutputStream.writeUTF(file.getName());
        dataOutputStream.writeLong(file.length());

        byte[] buffer = new byte[4*1024];
        while ((bytes=fileInputStream.read(buffer))!=-1){
            dataOutputStream.write(buffer,0,bytes);
            dataOutputStream.flush();
        }
        fileInputStream.close();
    }
}