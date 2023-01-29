using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class tx_blocks : MonoBehaviour
{
    //Link "Parent" - object & "Block" - object(s)
    public Transform parent;
    public GameObject tx_block;
    public GameObject History_List;
    public void Create_History_View()
    {

        //Create 10 Blocks as children of "content" (scrollview)
        //1 Block  = 1 Transaction -> last 10 Transactions listed.
        //Daemon limitation may not be met yet.

        if (GameObject.FindGameObjectsWithTag("history_block_transaction").Length == 0)
        {

            Instantiate(tx_block, new Vector3(Screen.width/6, Screen.height*2/3, 0), parent.transform.rotation, parent);
            for (int i = 0; i < 9; i++)
            {
                GameObject[] blocks = GameObject.FindGameObjectsWithTag("history_block_transaction");
                Transform last_block = blocks[blocks.Length - 1].transform;
                Vector3 new_position = new Vector3(Screen.width/6, last_block.transform.position.y - Screen.height / 6, 0);
                Instantiate(tx_block, new_position, parent.transform.rotation, parent);
            }
        }
    }
}