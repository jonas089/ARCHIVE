using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class panel_c : MonoBehaviour
{
    // 1 = Ravencoin; 2 = Bitcoin; 3 = CryptOS
    public static int Currency_Chosen_For_Transaction = 0;
    /*
     Code to handle activity of all "Ledger" - panels
     Public = true
     Static = false
     */

    public GameObject bar;

    //Feedback panel(s)
    public GameObject Transaction_valid; // TBA
    public GameObject Transaction_failed; // TBA

    //Transaction - related panel(s)
    public GameObject transaction_panel;
    public GameObject transaction_history_panel;
    public GameObject Choose_Transaction_Currency_Panel;

    public GameObject Transaction_Type_Username_Or_Address_Element;

    public GameObject Address_panel;

    //ICO - related panel(s)
    public GameObject Choose_Currency_To_Buy_Panel;
    public GameObject Buy_With_Ravencoin_Panel;
    public GameObject Buy_With_Bitcoin_Panel;


    //Interface - related panel(s)
    public GameObject lock_panel;

    //On - Off method(s)
    public void transaction_panel_on()
    {
        if (Currency_Chosen_For_Transaction == 1 || Currency_Chosen_For_Transaction == 2)
        {
            transaction_panel.SetActive(true);
            Transaction_Type_Username_Or_Address_Element.SetActive(false);
            bar.SetActive(false);
        }
        else if (Currency_Chosen_For_Transaction == 3)
        {
            transaction_panel.SetActive(true);
            Transaction_Type_Username_Or_Address_Element.SetActive(true);
            bar.SetActive(false);
        }
    }
    public void transaction_panel_off()
    {
        transaction_panel.SetActive(false);
        bar.SetActive(true);
    }
    public void transaction_history_panel_on()
    {
        transaction_history_panel.SetActive(true);
    }
    public void transaction_history_panel_off()
    {
        transaction_history_panel.SetActive(false);
    }
    public void lock_panel_on()
    {
        lock_panel.SetActive(true);
        bar.SetActive(false);
    }
    public void lock_panel_off()
    {
        lock_panel.SetActive(false);
        bar.SetActive(true);
    }
    public void Transaction_failed_panel_off()
    {
        Transaction_failed.SetActive(false);
    }
    public void Transaction_valid_panel_off()
    {
        Transaction_valid.SetActive(false);
    }
    public void Address_panel_off()
    {
        Address_panel.SetActive(false);
    }
    public void Address_panel_on()
    {
        Address_panel.SetActive(true);
    }
    public void Choose_Transaction_History_Panel_On()
    {
        Choose_Transaction_Currency_Panel.SetActive(true);
    }
    public void Choose_Transaction_History_Panel_Off()
    {
        Choose_Transaction_Currency_Panel.SetActive(false);
    }
    public void Ravencoin_Currency_Chosen_For_Transaction()
    {
        Currency_Chosen_For_Transaction = 1;
    }
    public void Bitcoin_Currency_Chosen_For_Transaction()
    {
        Currency_Chosen_For_Transaction = 2;
    }
    public void CryOS_Currency_Chosen_For_Transaction()
    {
        Currency_Chosen_For_Transaction = 3;
    }
    public void Choose_Currency_To_Buy_Panel_On()
    {
        Choose_Currency_To_Buy_Panel.SetActive(true);
    }
    public void Choose_Currency_To_Buy_Panel_Off()
    {
        Choose_Currency_To_Buy_Panel.SetActive(false);
    }
    public void Buy_With_Ravencoin_Panel_On()
    {
        Buy_With_Ravencoin_Panel.SetActive(true);
    }
    public void Buy_With_Ravencoin_Panel_Off()
    {
        Buy_With_Ravencoin_Panel.SetActive(false);
    }
    public void Buy_With_Bitcoin_Panel_On()
    {
        Buy_With_Bitcoin_Panel.SetActive(true);
    }
    public void Buy_With_Bitcoin_Panel_Off()
    {
        Buy_With_Bitcoin_Panel.SetActive(false);
    }
}
